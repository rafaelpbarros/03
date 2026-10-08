"""Extrai os arquivos FoxPro em dados_extraidos para um banco SQLite local.

Instale a dependencia com: pip install -r requirements.txt
Execute com: python inicio.py
"""

import csv
import os
import sqlite3
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from dbfread import DBF
from dbfread.field_parser import FieldParser

from config_sistema import (
    ARQUIVO_RELATORIO_SQLITE,
    ARQUIVO_SQLITE,
    PASTA_DADOS,
    garantir_pastas_de_saida,
)
from relatorios import agora, finalizar_execucao, iniciar_execucao, registrar_tabela


TAMANHO_LOTE = 10_000
TRABALHADORES = min(os.cpu_count() or 1, 12)


class ParserTolerante(FieldParser):
    """Mantem o registro quando um campo FoxPro possui valor invalido."""

    def __init__(self, table, memofile=None):
        super().__init__(table, memofile)
        table.alertas_extracao = Counter()

    def registrar_alerta(self, categoria: str, campo) -> None:
        self.table.alertas_extracao[f"{categoria}:{campo.name}"] += 1

    def decode_text(self, text):
        try:
            return super().decode_text(text)
        except UnicodeDecodeError:
            self.table.alertas_extracao["texto_com_bytes_invalidos"] += 1
            return text.decode(self.encoding, errors="replace")

    def parseD(self, field, data):
        try:
            return super().parseD(field, data)
        except ValueError:
            self.registrar_alerta("data_invalida_convertida_em_nulo", field)
            return None

    def parseL(self, field, data):
        try:
            return super().parseL(field, data)
        except ValueError:
            self.registrar_alerta("logico_invalido_convertido_em_nulo", field)
            return None

    def parseN(self, field, data):
        try:
            return super().parseN(field, data)
        except ValueError:
            self.registrar_alerta("numero_invalido_convertido_em_nulo", field)
            return None

    def parseF(self, field, data):
        try:
            return super().parseF(field, data)
        except ValueError:
            self.registrar_alerta("numero_invalido_convertido_em_nulo", field)
            return None

    def parseM(self, field, data):
        try:
            indice = self._parse_memo_index(data)
        except ValueError:
            self.registrar_alerta("indice_memo_invalido_convertido_em_nulo", field)
            return None

        memo = super().parseM(field, data)
        if memo is None and indice:
            self.registrar_alerta("memo_indisponivel_convertido_em_nulo", field)
        return memo


def identificar(nome: str) -> str:
    """Escapa um identificador SQLite, como nome de tabela ou coluna."""
    return f'"{nome.replace("\"", "\"\"")}"'


def valor_sqlite(valor):
    """Converte valores FoxPro para tipos que o SQLite aceita diretamente."""
    if valor is None or isinstance(valor, (bytes, str, int, float)):
        return valor
    if isinstance(valor, bool):
        return int(valor)
    if isinstance(valor, (date, datetime)):
        return valor.isoformat(sep=" ") if isinstance(valor, datetime) else valor.isoformat()
    if isinstance(valor, Decimal):
        return str(valor)
    return str(valor)


def nome_tabela(dbf: Path, nomes_usados: set[str]) -> str:
    """Mantem o nome do DBF e evita colisao de nomes no SQLite."""
    base = dbf.stem
    nome = base
    contador = 2
    while nome.casefold() in nomes_usados:
        nome = f"{base}_{contador}"
        contador += 1
    nomes_usados.add(nome.casefold())
    return nome


def criar_tabela(conexao: sqlite3.Connection, tabela: str, colunas: list[str]) -> None:
    definicoes = ", ".join(f"{identificar(coluna)} TEXT" for coluna in colunas)
    conexao.execute(f"CREATE TABLE {identificar(tabela)} ({definicoes})")


def configurar_carga_rapida(conexao: sqlite3.Connection) -> None:
    conexao.execute("PRAGMA journal_mode = OFF")
    conexao.execute("PRAGMA synchronous = OFF")
    conexao.execute("PRAGMA temp_store = MEMORY")
    conexao.execute("PRAGMA cache_size = -262144")


def extrair_tabela(dbf: Path, tabela: str, arquivo_temporario: Path) -> dict[str, object]:
    resultado = {
        "arquivo_dbf": dbf.name,
        "tabela_sqlite": tabela,
        "status": "FALHA",
        "registros_fisicos": "",
        "registros_ativos_lidos": 0,
        "registros_gravados": 0,
        "alertas_de_dados": "",
        "erro": "",
        "inicio_tabela": agora(),
        "fim_tabela": "",
        "duracao_tabela_segundos": "",
    }
    inicio_medicao = perf_counter()

    try:
        with sqlite3.connect(arquivo_temporario) as conexao:
            configurar_carga_rapida(conexao)
            _extrair_tabela_no_arquivo(conexao, dbf, tabela, resultado)
    except Exception as erro:
        resultado["status"] = "PARCIAL_DESCARTADA" if resultado["registros_ativos_lidos"] else "FALHA"
        resultado["erro"] = f"{type(erro).__name__}: {erro}"
    finally:
        resultado["fim_tabela"] = agora()
        resultado["duracao_tabela_segundos"] = f"{perf_counter() - inicio_medicao:.3f}"

    return resultado


def _extrair_tabela_no_arquivo(
    conexao: sqlite3.Connection, dbf: Path, tabela: str, resultado: dict[str, object]
) -> None:
    try:
        leitor = DBF(
            dbf,
            encoding="cp1252",
            char_decode_errors="strict",
            parserclass=ParserTolerante,
            ignore_missing_memofile=True,
            load=False,
        )
        colunas = [campo.name for campo in leitor.fields]
        resultado["registros_fisicos"] = leitor.header.numrecords
        if not colunas:
            raise ValueError("O DBF nao possui colunas.")

        placeholders = ", ".join("?" for _ in colunas)
        comando_insercao = (
            f"INSERT INTO {identificar(tabela)} "
            f"({', '.join(identificar(coluna) for coluna in colunas)}) VALUES ({placeholders})"
        )

        conexao.execute("BEGIN")
        criar_tabela(conexao, tabela, colunas)
        lote = []
        for registro in leitor:
            lote.append(tuple(valor_sqlite(registro[coluna]) for coluna in colunas))
            resultado["registros_ativos_lidos"] += 1
            if len(lote) == TAMANHO_LOTE:
                conexao.executemany(comando_insercao, lote)
                resultado["registros_gravados"] += len(lote)
                lote.clear()

        if lote:
            conexao.executemany(comando_insercao, lote)
            resultado["registros_gravados"] += len(lote)

        total_sqlite = conexao.execute(
            f"SELECT COUNT(*) FROM {identificar(tabela)}"
        ).fetchone()[0]
        if total_sqlite != resultado["registros_ativos_lidos"]:
            raise RuntimeError(
                f"Contagem divergente: lidos={resultado['registros_ativos_lidos']}, "
                f"SQLite={total_sqlite}."
            )

        conexao.commit()
        alertas = getattr(leitor, "alertas_extracao", Counter())
        resultado["alertas_de_dados"] = ", ".join(
            f"{alerta}={quantidade}" for alerta, quantidade in sorted(alertas.items())
        )
        resultado["status"] = "OK_COM_ALERTAS" if alertas else "OK"
    except Exception as erro:
        conexao.rollback()
        raise RuntimeError(f"{type(erro).__name__}: {erro}") from erro


def consolidar_tabela(
    conexao: sqlite3.Connection, tabela: str, arquivo_temporario: Path
) -> int:
    conexao.execute("ATTACH DATABASE ? AS origem", (str(arquivo_temporario),))
    try:
        colunas = [
            linha[1]
            for linha in conexao.execute(f"PRAGMA origem.table_info({identificar(tabela)})")
        ]
        criar_tabela(conexao, tabela, colunas)
        conexao.execute(
            f"INSERT INTO {identificar(tabela)} SELECT * FROM origem.{identificar(tabela)}"
        )
        total = conexao.execute(f"SELECT COUNT(*) FROM {identificar(tabela)}").fetchone()[0]
        conexao.commit()
        return total
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.execute("DETACH DATABASE origem")


def salvar_relatorio(resultados: list[dict[str, object]]) -> None:
    colunas = [
        "arquivo_dbf",
        "tabela_sqlite",
        "status",
        "registros_fisicos",
        "registros_ativos_lidos",
        "registros_gravados",
        "alertas_de_dados",
        "erro",
        "inicio_tabela",
        "fim_tabela",
        "duracao_tabela_segundos",
    ]
    with ARQUIVO_RELATORIO_SQLITE.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
        escritor.writeheader()
        escritor.writerows(resultados)


def main() -> None:
    garantir_pastas_de_saida()
    inicio_execucao, inicio_medicao = iniciar_execucao("SQLite")
    if not PASTA_DADOS.is_dir():
        raise FileNotFoundError(f"Pasta de dados nao encontrada: {PASTA_DADOS}")

    arquivos_dbf = sorted(PASTA_DADOS.glob("*.[dD][bB][fF]"), key=lambda arquivo: arquivo.name.casefold())
    if not arquivos_dbf:
        raise FileNotFoundError(f"Nenhum arquivo DBF encontrado em: {PASTA_DADOS}")

    ARQUIVO_SQLITE.unlink(missing_ok=True)
    resultados = []
    nomes_usados = set()
    tarefas = [
        (dbf, nome_tabela(dbf, nomes_usados))
        for dbf in arquivos_dbf
    ]

    with TemporaryDirectory(prefix="etl_foxpro_") as diretorio_temporario:
        pasta_temporaria = Path(diretorio_temporario)
        arquivos_temporarios = {}
        with ProcessPoolExecutor(max_workers=TRABALHADORES) as executor:
            futuros = {
                executor.submit(
                    extrair_tabela,
                    dbf,
                    tabela,
                    pasta_temporaria / f"{indice:03d}.db",
                ): (indice, dbf, tabela)
                for indice, (dbf, tabela) in enumerate(tarefas)
            }
            for futuro in as_completed(futuros):
                indice, dbf, tabela = futuros[futuro]
                resultado = futuro.result()
                resultados.append(resultado)
                registrar_tabela("SQLite", resultado)
                if str(resultado["status"]).startswith("OK"):
                    arquivos_temporarios[tabela] = pasta_temporaria / f"{indice:03d}.db"
                print(
                    f"{resultado['status']}: {dbf.name} "
                    f"({resultado['duracao_tabela_segundos']}s)"
                )

        with sqlite3.connect(ARQUIVO_SQLITE) as conexao:
            configurar_carga_rapida(conexao)
            for resultado in resultados:
                if not str(resultado["status"]).startswith("OK"):
                    continue
                total_sqlite = consolidar_tabela(
                    conexao,
                    str(resultado["tabela_sqlite"]),
                    arquivos_temporarios[str(resultado["tabela_sqlite"])],
                )
                if total_sqlite != resultado["registros_gravados"]:
                    raise RuntimeError(
                        f"Contagem divergente ao consolidar {resultado['tabela_sqlite']}."
                    )
            conexao.commit()

    resultados.sort(key=lambda resultado: str(resultado["arquivo_dbf"]).casefold())
    salvar_relatorio(resultados)
    tempo_execucao = finalizar_execucao(
        "SQLite", inicio_execucao, inicio_medicao, resultados
    )
    completos = sum(str(resultado["status"]).startswith("OK") for resultado in resultados)
    com_alertas = sum(resultado["status"] == "OK_COM_ALERTAS" for resultado in resultados)
    incompletos = len(resultados) - completos
    print(f"\nTabelas completas: {completos}")
    print(f"Tabelas completas com alertas de dados: {com_alertas}")
    print(f"Tabelas com falha ou extracao parcial: {incompletos}")
    print(f"Processos paralelos: {TRABALHADORES}")
    print(f"SQLite: {ARQUIVO_SQLITE}")
    print(f"Inicio da execucao: {inicio_execucao}")
    print(f"Tempo total de execucao: {tempo_execucao:.3f}s")
    print(f"Relatorio: {ARQUIVO_RELATORIO_SQLITE}")


if __name__ == "__main__":
    main()
