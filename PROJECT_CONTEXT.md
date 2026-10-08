# Contexto do Projeto

## Identificacao

- Projeto: Plataforma de extracao FoxPro DBF para analise.
- Objetivo de negocio: disponibilizar dados extraidos de arquivos DBF em camadas confiaveis para consulta no Metabase.
- Ultima atualizacao: 2026-10-08.

## Escopo e Restricoes

- Entradas: arquivos DBF/FoxPro em `dados_extraidos/`.
- Saidas atuais: `vet.db` (SQLite Bronze) e schema PostgreSQL `dbf_importacao` (Silver).
- Consumidor planejado: Metabase sobre a camada Gold.
- Restricoes: operacao local com Docker durante o desenvolvimento; futura execucao em servidor Ubuntu; configuracao sensivel via `.env`.
- Fora do escopo atual: exposicao publica, dados de exemplo e uso da rota direta DBF para PostgreSQL em producao.

## Arquitetura Atual

- Bronze: `dbf_to_sqlite.py` extrai arquivos DBF para `vet.db`.
- Silver: `sqlite_to_postgres.py` carrega todas as tabelas do SQLite para PostgreSQL com `asyncpg.copy_records_to_table`.
- Observabilidade: relatorios CSV por execucao e `relatorio_consolidado.log`.
- Infraestrutura local: `docker-compose.yml` executa PostgreSQL 17 Alpine em `localhost:5433`.
- Orquestracao planejada: Airflow com `LocalExecutor` e banco de metadados dedicado.
- Requisitos de negocio: documentos PDF em `consultoria/` descrevem BSC, indicadores, PDCA e declaracoes estrategicas.
- Catalogo de metricas: `consultoria/CATALOGO_METRICAS_DW_METABASE.md` prioriza 38 metricas por relevancia e disponibilidade no ERP.
- Coleta manual: `consultoria/COLETA_MANUAL_METRICAS_METABASE.md` lista informacoes ausentes no ERP e `sql/coleta_manual_metricas.sql` preserva seu historico no schema Gold.

## Decisoes Registradas

| Data | Decisao | Motivo | Impacto | Status |
| --- | --- | --- | --- | --- |
| 2026-10-08 | Usar SQLite como area de staging entre DBF e PostgreSQL. | O caminho em duas etapas foi mais rapido e oferece uma fronteira de recuperacao. | O fluxo operacional recomendado passa por Bronze e Silver. | Confirmada |
| 2026-10-08 | Usar `asyncpg` e COPY binario para carga no PostgreSQL. | Evita limitacoes observadas em drivers anteriores e melhora a carga em lote. | O carregador Silver depende de `asyncpg`. | Confirmada |
| 2026-10-08 | Adotar Docker Compose para PostgreSQL local. | Permite testes reproduziveis sem depender de instalacao local do banco. | O PostgreSQL de desenvolvimento responde na porta 5433. | Confirmada |
| 2026-10-08 | Planejar Airflow para orquestracao futura. | Separa agendamento, tentativas e observabilidade da logica ETL. | Requer desenho e aprovacao antes de adicionar servicos ao Compose. | Pendente |
| 2026-10-08 | Usar os documentos em `consultoria/` como fonte inicial dos requisitos de dashboard. | Eles registram as perspectivas BSC, objetivos, metas e indicadores do hospital. | O catalogo Gold deve mapear cada indicador a formula, fonte e responsavel. | Confirmada |
| 2026-10-08 | Priorizar metricas por impacto estrategico, economico, acionabilidade, pratica de mercado e viabilidade no ERP. | Evita construir primeiro indicadores de baixa utilidade ou que exigem nova captura. | O primeiro ciclo do dashboard deve conter somente metricas P0 com regra aprovada. | Pendente aprovacao |
| 2026-10-08 | Registrar valores nao disponiveis no ERP em coleta manual versionada. | Evita inferir CSAT, RH, PDCA, baselines ou metas a partir de DBFs inadequados. | O dashboard pode combinar fatos automaticos e valores manuais rastreaveis. | Confirmada |

## Estado da Etapa Atual

- Etapa: Fundacao do processo de desenvolvimento (concluida).
- Objetivo imediato: aprovar metricas P0 e iniciar seu mapeamento fisico para a camada Gold.
- Entrega concluida: prompts do VS Code e templates de contexto.
- Criterio de aceite: atendido; os artefatos possuem frontmatter valido, estao nos caminhos esperados e nao contem segredos.
- Riscos ou bloqueios: a camada Gold, Metabase e Airflow ainda nao foram implementados.

## Validacoes Executadas

| Data | Mudanca ou entrega | Validacao | Resultado | Evidencia |
| --- | --- | --- | --- | --- |
| 2026-10-08 | Carga Silver SQLite para PostgreSQL. | Execucao completa contra PostgreSQL em Docker. | 280 tabelas concluidas em 99.047 segundos. | `relatorio_consolidado.log` |
| 2026-10-08 | Banco PostgreSQL local. | Healthcheck do Compose. | Servico saudavel. | `docker-compose.yml` |
| 2026-10-08 | Prompt reutilizavel e contexto do projeto. | Verificacao de caminhos, frontmatter e ausencia de segredos. | Aprovada sem achados. | `.github/prompts/` e perfil de usuario do VS Code |
| 2026-10-08 | Documentos de consultoria. | Leitura dos PDFs BSC, indicadores/PDCA e missao/visao/valores. | Objetivos e metas identificados; formulas, linhas de base e fontes ainda precisam ser definidos. | `consultoria/` |
| 2026-10-08 | Catalogo de metricas DW/Metabase. | Verificacao de 38 ranks unicos, prioridades P0/P1/P2 e rotulos de disponibilidade. | Aprovado tecnicamente; relevancia de negocio pendente de aprovacao. | `consultoria/CATALOGO_METRICAS_DW_METABASE.md` |
| 2026-10-08 | Estrutura de coleta manual. | Execucao do SQL em transacao revertida no PostgreSQL local. | Schema, tabela e view validos; nenhum dado de exemplo inserido. | `sql/coleta_manual_metricas.sql` |

## Proximo Passo

- Acao proposta: aprovar o conjunto P0 e mapear cada metrica para tabelas, campos e regras de transformacao de origem.
- Decisao que exige aprovacao: quais metricas P0 entrarao no primeiro dashboard e quais metas numericas deverao ser oficializadas.
- Informacoes necessarias: linha de base, formula, responsavel, periodicidade, fonte de cada indicador aprovado e valores definidos em `COLETA_MANUAL_METRICAS_METABASE.md`.