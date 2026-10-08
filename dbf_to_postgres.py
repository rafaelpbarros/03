"""Extrai arquivos FoxPro em dados_extraidos para um banco PostgreSQL.

Configure as variaveis POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE,
POSTGRES_USER, POSTGRES_PASSWORD e, opcionalmente, POSTGRES_SCHEMA.
Instale as dependencias com: pip install -r requirements.txt
Execute com: python dbf_to_postgres.py
"""

import asyncio
import csv
from collections import Counter
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from time import perf_counter

import asyncpg
from dbfread import DBF
from dbfread.field_parser import FieldParser

from comandos_sql import (
    contar_registros,
    criar_schema,
    criar_tabela,
    remover_schema,
    remover_tabela,
)
from config_banco import (
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_SCHEMA,
    parametros_conexao,
)
from config_sistema import (
    ARQUIVO_RELATORIO_POSTGRES,
    CONCORRENCIA_POSTGRES,
    PASTA_DADOS,
    garantir_pastas_de_saida,
)
from relatorios import agora, finalizar_execucao, iniciar_execucao, registrar_tabela


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


def valor_postgres(valor, alertas: Counter) -> str | None:
    """Converte valores FoxPro para texto, preservando a carga uniforme das colunas."""
    if valor is None:
        return None
    if isinstance(valor, bool):
        return "1" if valor else "0"
    if isinstance(valor, (date, datetime)):
        return valor.isoformat(sep=" ") if isinstance(valor, datetime) else valor.isoformat()
    if isinstance(valor, Decimal):
        return str(valor)
    if isinstance(valor, bytes):
        texto = valor.decode("cp1252", errors="replace")
    else:
        texto = str(valor)

    quantidade_nulos = texto.count("\x00")
    if quantidade_nulos:
        alertas["byte_nulo_removido"] += quantidade_nulos
        texto = texto.replace("\x00", "")
    return texto


def nome_tabela(dbf: Path, nomes_usados: set[str]) -> str:
    """Mantem o nome do DBF e evita colisao de nomes no PostgreSQL."""
    base = dbf.stem
    nome = base
    contador = 2
    while nome.casefold() in nomes_usados:
        nome = f"{base}_{contador}"
        contador += 1
    nomes_usados.add(nome.casefold())
    return nome


def registros_copy(leitor, colunas: list[str], resultado: dict[str, object]):
    """Produz registros para o COPY binario sem acumular a tabela em memoria."""
    for registro in leitor:
        yield tuple(
            valor_postgres(registro[coluna], resultado["alertas_de_carga"])
            for coluna in colunas
        )
        resultado["registros_ativos_lidos"] += 1


async def carregar_tabela(pool, dbf: Path, tabela: str) -> dict[str, object]:
    resultado = {
        "arquivo_dbf": dbf.name,
        "tabela_postgres": tabela,
        "status": "FALHA",
        "registros_fisicos": "",
        "registros_ativos_lidos": 0,
        "registros_gravados": 0,
        "alertas_de_dados": "",
        "erro": "",
        "inicio_tabela": agora(),
        "fim_tabela": "",
        "duracao_tabela_segundos": "",
        "alertas_de_carga": Counter(),
    }
    inicio_medicao = perf_counter()

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

        async with pool.acquire() as conexao:
            async with conexao.transaction():
                await conexao.execute(criar_tabela(POSTGRES_SCHEMA, tabela, colunas))
                await conexao.copy_records_to_table(
                    tabela,
                    records=registros_copy(leitor, colunas, resultado),
                    columns=colunas,
                    schema_name=POSTGRES_SCHEMA,
                )
                resultado["registros_gravados"] = resultado["registros_ativos_lidos"]

                total_postgres = await conexao.fetchval(contar_registros(POSTGRES_SCHEMA, tabela))
                if total_postgres != resultado["registros_ativos_lidos"]:
                    raise RuntimeError(
                        f"Contagem divergente: lidos={resultado['registros_ativos_lidos']}, "
                        f"PostgreSQL={total_postgres}."
                    )

        alertas = getattr(leitor, "alertas_extracao", Counter())
        alertas.update(resultado["alertas_de_carga"])
        resultado["alertas_de_dados"] = ", ".join(
            f"{alerta}={quantidade}" for alerta, quantidade in sorted(alertas.items())
        )
        resultado["status"] = "OK_COM_ALERTAS" if alertas else "OK"
    except Exception as erro:
        resultado["status"] = "PARCIAL_DESCARTADA" if resultado["registros_ativos_lidos"] else "FALHA"
        resultado["erro"] = f"{type(erro).__name__}: {erro}"
    finally:
        resultado["fim_tabela"] = agora()
        resultado["duracao_tabela_segundos"] = f"{perf_counter() - inicio_medicao:.3f}"

    return resultado


def salvar_relatorio(resultados: list[dict[str, object]]) -> None:
    colunas = [
        "arquivo_dbf", "tabela_postgres", "status", "registros_fisicos",
        "registros_ativos_lidos", "registros_gravados", "alertas_de_dados", "erro",
        "inicio_tabela", "fim_tabela", "duracao_tabela_segundos",
    ]
    with ARQUIVO_RELATORIO_POSTGRES.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=colunas, delimiter=";", extrasaction="ignore"
        )
        escritor.writeheader()
        escritor.writerows(resultados)


async def main_async() -> None:
    garantir_pastas_de_saida()
    inicio_execucao, inicio_medicao = iniciar_execucao("PostgreSQL")
    if not PASTA_DADOS.is_dir():
        raise FileNotFoundError(f"Pasta de dados nao encontrada: {PASTA_DADOS}")

    arquivos_dbf = sorted(PASTA_DADOS.glob("*.[dD][bB][fF]"), key=lambda arquivo: arquivo.name.casefold())
    if not arquivos_dbf:
        raise FileNotFoundError(f"Nenhum arquivo DBF encontrado em: {PASTA_DADOS}")

    nomes_usados: set[str] = set()
    tarefas = [(dbf, nome_tabela(dbf, nomes_usados)) for dbf in arquivos_dbf]
    resultados = []
    if CONCORRENCIA_POSTGRES < 1:
        raise ValueError("POSTGRES_CONCURRENCY deve ser maior que zero.")

    pool = await asyncpg.create_pool(
        **parametros_conexao(), min_size=1, max_size=CONCORRENCIA_POSTGRES
    )
    try:
        async with pool.acquire() as conexao:
            await conexao.execute(remover_schema(POSTGRES_SCHEMA))
            await conexao.execute(criar_schema(POSTGRES_SCHEMA))

        tarefas_carga = [
            asyncio.create_task(carregar_tabela(pool, dbf, tabela))
            for dbf, tabela in tarefas
        ]
        for tarefa in asyncio.as_completed(tarefas_carga):
            resultado = await tarefa
            resultados.append(resultado)
            registrar_tabela("PostgreSQL", resultado)
            print(
                f"{resultado['status']}: {resultado['arquivo_dbf']} "
                f"({resultado['duracao_tabela_segundos']}s)"
            )
    finally:
        await pool.close()

    resultados.sort(key=lambda resultado: str(resultado["arquivo_dbf"]).casefold())
    salvar_relatorio(resultados)
    tempo_execucao = finalizar_execucao(
        "PostgreSQL", inicio_execucao, inicio_medicao, resultados
    )
    completos = sum(str(resultado["status"]).startswith("OK") for resultado in resultados)
    com_alertas = sum(resultado["status"] == "OK_COM_ALERTAS" for resultado in resultados)
    print(f"\nTabelas completas: {completos}")
    print(f"Tabelas completas com alertas de dados: {com_alertas}")
    print(f"Tabelas com falha ou extracao parcial: {len(resultados) - completos}")
    print(f"PostgreSQL: {POSTGRES_DATABASE}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_SCHEMA}")
    print(f"Conexoes paralelas: {CONCORRENCIA_POSTGRES}")
    print(f"Inicio da execucao: {inicio_execucao}")
    print(f"Tempo total de execucao: {tempo_execucao:.3f}s")
    print(f"Relatorio: {ARQUIVO_RELATORIO_POSTGRES}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()