# Operacao Local

## Pre-requisitos

- Python 3.12 ou compativel.
- Docker Desktop com Compose.
- DBFs exportados pelo ERP em `dados_extraidos/`.

## Configuracao

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
docker compose up -d
```

O `.env` e local e nunca deve ser versionado. Para o Compose atual, use porta `5433`, banco `postgres`, usuario `postgres` e a senha definida localmente.

## Execucao recomendada

```powershell
.\.venv\Scripts\python.exe .\dbf_to_sqlite.py
.\.venv\Scripts\python.exe .\sqlite_to_postgres.py
```

Resultados esperados:

- Bronze em `data/bronze/vet.db`.
- CSVs e log em `reports/`.
- Tabelas Silver no schema indicado por `POSTGRES_SCHEMA`.

## Verificacao basica

```powershell
docker compose ps
Get-Content .\reports\relatorio_consolidado.log -Tail 20
```

O carregador Silver valida que a contagem PostgreSQL coincide com o total lido do SQLite por tabela.

## Recuperacao

- Falha Bronze: corrigir a origem ou analisar `reports/relatorio_extracao_sqlite.csv`; a proxima execucao recria o SQLite.
- Falha Silver: analisar `reports/relatorio_copia_sqlite_postgres.csv`; a proxima execucao recria apenas o schema Silver configurado.
- Nunca execute os scripts contra um schema que contenha dados de producao nao descartaveis.

## Rotina de Git

```powershell
git status
git add README.md docs sql consultoria templates .github *.py requirements.txt docker-compose.yml .env.example PROJECT_CONTEXT.md .gitignore
git commit -m "docs: establish project foundation"
```

Antes de qualquer `git add`, confirme que DBFs, bancos SQLite, relatorios e `.env` aparecem como ignorados.