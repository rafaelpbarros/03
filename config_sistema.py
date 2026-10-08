"""Configuracoes locais da extracao dos arquivos DBF."""

import os
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados_extraidos"
PASTA_DADOS_BRONZE = PASTA_PROJETO / "data" / "bronze"
PASTA_RELATORIOS = PASTA_PROJETO / "reports"
ARQUIVO_SQLITE = PASTA_DADOS_BRONZE / "vet.db"
ARQUIVO_RELATORIO_SQLITE = PASTA_RELATORIOS / "relatorio_extracao_sqlite.csv"
ARQUIVO_RELATORIO_POSTGRES = PASTA_RELATORIOS / "relatorio_extracao_postgres.csv"
ARQUIVO_RELATORIO_SQLITE_POSTGRES = PASTA_RELATORIOS / "relatorio_copia_sqlite_postgres.csv"
ARQUIVO_LOG_CONSOLIDADO = PASTA_RELATORIOS / "relatorio_consolidado.log"
TRABALHADORES = min(os.cpu_count() or 1, 12)
CONCORRENCIA_POSTGRES = int(os.getenv("POSTGRES_CONCURRENCY", "4"))


def garantir_pastas_de_saida() -> None:
	"""Cria as pastas locais usadas pelos artefatos gerados do ETL."""
	PASTA_DADOS_BRONZE.mkdir(parents=True, exist_ok=True)
	PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)