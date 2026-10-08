# Registro de Decisoes

| Data | Decisao | Contexto | Consequencia |
| --- | --- | --- | --- |
| 2026-10-08 | Usar SQLite como Bronze. | A carga em duas etapas foi mais rapida e recuperavel. | O fluxo recomendado e DBF para SQLite e SQLite para PostgreSQL. |
| 2026-10-08 | Usar `asyncpg` com COPY binario na Silver. | Melhor desempenho e menos limitacoes na carga em lote. | A Silver depende de `asyncpg`. |
| 2026-10-08 | Usar Docker Compose para PostgreSQL local. | Desenvolvimento reproduzivel. | PostgreSQL local na porta 5433. |
| 2026-10-08 | Manter coletas manuais versionadas no Gold. | Algumas metricas BSC nao existem no ERP. | Metas, pesquisas, RH e PDCA nao serao inferidos de DBFs. |
| 2026-10-08 | Organizar artefatos gerados fora da raiz e inicializar Git. | Melhor navegacao e protecao contra versionar dados e segredos. | SQLite em `data/bronze/`; relatorios em `reports/`; dados e segredos ignorados. |