"""Registro dos tempos de carga em CSVs individuais e um log consolidado."""

from datetime import datetime
from time import perf_counter

from config_sistema import ARQUIVO_LOG_CONSOLIDADO


def agora() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def iniciar_execucao(solucao: str) -> tuple[str, float]:
    inicio = agora()
    registrar_linha(f"INICIO solucao={solucao} inicio={inicio}")
    return inicio, perf_counter()


def registrar_tabela(solucao: str, resultado: dict[str, object]) -> None:
    registrar_linha(
        "TABELA "
        f"solucao={solucao} arquivo={resultado['arquivo_dbf']} "
        f"tabela={resultado.get('tabela_sqlite', resultado.get('tabela_postgres', ''))} "
        f"status={resultado['status']} inicio={resultado['inicio_tabela']} "
        f"fim={resultado['fim_tabela']} "
        f"duracao_segundos={resultado['duracao_tabela_segundos']} "
        f"registros={resultado['registros_gravados']}"
    )


def finalizar_execucao(solucao: str, inicio: str, inicio_medicao: float, resultados) -> float:
    duracao = perf_counter() - inicio_medicao
    fim = agora()
    completos = sum(str(resultado["status"]).startswith("OK") for resultado in resultados)
    registrar_linha(
        f"FIM solucao={solucao} inicio={inicio} fim={fim} "
        f"duracao_segundos={duracao:.3f} tabelas={len(resultados)} "
        f"completas={completos} incompletas={len(resultados) - completos}"
    )
    return duracao


def registrar_linha(linha: str) -> None:
    with ARQUIVO_LOG_CONSOLIDADO.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"{linha}\n")