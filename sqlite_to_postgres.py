"""Copia todas as tabelas de vet.db para PostgreSQL usando asyncpg COPY binario."""

import asyncio
import csv
import sqlite3
from collections import Counter
from pathlib import Path
from time import perf_counter

import asyncpg

from comandos_sql import contar_registros, criar_schema, criar_tabela, remover_schema
from config_banco import (
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_SCHEMA,
    parametros_conexao,
)
from config_sistema import (
    ARQUIVO_RELATORIO_SQLITE_POSTGRES,
    ARQUIVO_SQLITE,
    garantir_pastas_de_saida,
)
from relatorios import agora, finalizar_execucao, iniciar_execucao, registrar_tabela


TAMANHO_LOTE = 10_000


def identificar_sqlite(nome: str) -> str:
    return f'"{nome.replace("\"", "\"\"")}"'


def converter_valor(valor, alertas: Counter) -> str | None:
    if valor is None:
        return None
    if isinstance(valor, bytes):
        texto = valor.decode("cp1252", errors="replace")
    else:
        texto = str(valor)

    quantidade_nulos = texto.count("\x00")
    if quantidade_nulos:
        alertas["byte_nulo_removido"] += quantidade_nulos
        texto = texto.replace("\x00", "")
    return texto


def registros_sqlite(
    conexao: sqlite3.Connection,
    tabela: str,
    colunas: list[str],
    resultado: dict[str, object],
):
    consulta = (
        f"SELECT {', '.join(identificar_sqlite(coluna) for coluna in colunas)} "
        f"FROM {identificar_sqlite(tabela)}"
    )
    cursor = conexao.execute(consulta)
    while lote := cursor.fetchmany(TAMANHO_LOTE):
        for registro in lote:
            resultado["registros_lidos"] += 1
            yield tuple(converter_valor(valor, resultado["alertas_de_carga"]) for valor in registro)


async def copiar_tabela(
    conexao_postgres, conexao_sqlite: sqlite3.Connection, tabela: str
) -> dict[str, object]:
    resultado = {
        "arquivo_dbf": ARQUIVO_SQLITE.name,
        "tabela_postgres": tabela,
        "status": "FALHA",
        "registros_lidos": 0,
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
        colunas = [
            linha[1]
            for linha in conexao_sqlite.execute(
                f"PRAGMA table_info({identificar_sqlite(tabela)})"
            )
        ]
        if not colunas:
            raise ValueError("A tabela SQLite nao possui colunas.")

        async with conexao_postgres.transaction():
            await conexao_postgres.execute(criar_tabela(POSTGRES_SCHEMA, tabela, colunas))
            await conexao_postgres.copy_records_to_table(
                tabela,
                records=registros_sqlite(conexao_sqlite, tabela, colunas, resultado),
                columns=colunas,
                schema_name=POSTGRES_SCHEMA,
            )
            resultado["registros_gravados"] = resultado["registros_lidos"]
            total_postgres = await conexao_postgres.fetchval(
                contar_registros(POSTGRES_SCHEMA, tabela)
            )
            if total_postgres != resultado["registros_lidos"]:
                raise RuntimeError(
                    f"Contagem divergente: SQLite={resultado['registros_lidos']}, "
                    f"PostgreSQL={total_postgres}."
                )

        alertas = resultado["alertas_de_carga"]
        resultado["alertas_de_dados"] = ", ".join(
            f"{alerta}={quantidade}" for alerta, quantidade in sorted(alertas.items())
        )
        resultado["status"] = "OK_COM_ALERTAS" if alertas else "OK"
    except Exception as erro:
        resultado["status"] = "PARCIAL_DESCARTADA" if resultado["registros_lidos"] else "FALHA"
        resultado["erro"] = f"{type(erro).__name__}: {erro}"
    finally:
        resultado["fim_tabela"] = agora()
        resultado["duracao_tabela_segundos"] = f"{perf_counter() - inicio_medicao:.3f}"

    return resultado


def salvar_relatorio(resultados: list[dict[str, object]]) -> None:
    colunas = [
        "arquivo_dbf", "tabela_postgres", "status", "registros_lidos",
        "registros_gravados", "alertas_de_dados", "erro", "inicio_tabela",
        "fim_tabela", "duracao_tabela_segundos",
    ]
    with ARQUIVO_RELATORIO_SQLITE_POSTGRES.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=colunas, delimiter=";", extrasaction="ignore"
        )
        escritor.writeheader()
        escritor.writerows(resultados)


async def main_async() -> None:
    garantir_pastas_de_saida()
    if not ARQUIVO_SQLITE.is_file():
        raise FileNotFoundError(f"Banco SQLite nao encontrado: {ARQUIVO_SQLITE}")

    inicio_execucao, inicio_medicao = iniciar_execucao("SQLite_para_PostgreSQL")
    with sqlite3.connect(ARQUIVO_SQLITE) as conexao_sqlite:
        tabelas = [
            linha[0]
            for linha in conexao_sqlite.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        conexao_postgres = await asyncpg.connect(**parametros_conexao())
        try:
            await conexao_postgres.execute(remover_schema(POSTGRES_SCHEMA))
            await conexao_postgres.execute(criar_schema(POSTGRES_SCHEMA))

            resultados = []
            for tabela in tabelas:
                resultado = await copiar_tabela(conexao_postgres, conexao_sqlite, tabela)
                resultados.append(resultado)
                registrar_tabela("SQLite_para_PostgreSQL", resultado)
                print(
                    f"{resultado['status']}: {tabela} "
                    f"({resultado['duracao_tabela_segundos']}s)"
                )
        finally:
            await conexao_postgres.close()

    salvar_relatorio(resultados)
    tempo_execucao = finalizar_execucao(
        "SQLite_para_PostgreSQL", inicio_execucao, inicio_medicao, resultados
    )
    completos = sum(str(resultado["status"]).startswith("OK") for resultado in resultados)
    print(f"\nTabelas completas: {completos}")
    print(f"Tabelas com falha ou copia parcial: {len(resultados) - completos}")
    print(f"Inicio da execucao: {inicio_execucao}")
    print(f"Tempo total de execucao: {tempo_execucao:.3f}s")
    print(f"PostgreSQL: {POSTGRES_DATABASE}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_SCHEMA}")
    print(f"Relatorio: {ARQUIVO_RELATORIO_SQLITE_POSTGRES}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()