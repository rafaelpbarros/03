"""Comandos SQL usados pela carga para PostgreSQL."""



def identificar(nome: str) -> str:
    """Escapa um identificador PostgreSQL, como schema, tabela ou coluna."""
    return f'"{nome.replace("\"", "\"\"")}"'


def criar_schema(schema: str) -> str:
    return f"CREATE SCHEMA IF NOT EXISTS {identificar(schema)}"


def remover_schema(schema: str) -> str:
    return f"DROP SCHEMA IF EXISTS {identificar(schema)} CASCADE"


def remover_tabela(schema: str, tabela: str) -> str:
    return f"DROP TABLE IF EXISTS {identificar(schema)}.{identificar(tabela)} CASCADE"


def criar_tabela(schema: str, tabela: str, colunas: list[str]) -> str:
    definicoes = ", ".join(f"{identificar(coluna)} TEXT" for coluna in colunas)
    return f"CREATE TABLE {identificar(schema)}.{identificar(tabela)} ({definicoes})"


def copiar_registros(schema: str, tabela: str, colunas: list[str]) -> str:
    identificadores = ", ".join(identificar(coluna) for coluna in colunas)
    return (
        f"COPY {identificar(schema)}.{identificar(tabela)} "
        f"({identificadores}) FROM STDIN WITH (FORMAT text)"
    )


def contar_registros(schema: str, tabela: str) -> str:
    return f"SELECT COUNT(*) FROM {identificar(schema)}.{identificar(tabela)}"