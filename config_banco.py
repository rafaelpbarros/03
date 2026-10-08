"""Configuracao de acesso ao PostgreSQL.

Prefira definir as variaveis de ambiente para nao guardar credenciais no codigo.
"""

import os
from pathlib import Path


def carregar_arquivo_env() -> None:
    """Carrega variaveis ausentes do arquivo .env na pasta do projeto."""
    arquivo_env = Path(__file__).resolve().parent / ".env"
    if not arquivo_env.is_file():
        return

    for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", maxsplit=1)
        os.environ.setdefault(chave.strip(), valor.strip())


carregar_arquivo_env()


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "vet")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "dbf_importacao")


def parametros_conexao() -> dict[str, object]:
    """Retorna parametros compativeis com asyncpg."""
    return {
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
        "database": POSTGRES_DATABASE,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
    }