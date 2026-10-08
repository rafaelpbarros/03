# Camadas de Dados e Contratos

## Bronze: extracao fiel e rastreavel

- Entrada: arquivos DBF de `dados_extraidos/`.
- Saida: `data/bronze/vet.db`.
- Regra: uma tabela por DBF, mantendo nomes de campos e convertendo valores para tipos suportados pelo SQLite.
- Qualidade: contagem de registros e alertas por tabela em `reports/`.
- Reprocessamento: a cada execucao, o SQLite Bronze anterior e recriado.

## Silver: estrutura consultavel no PostgreSQL

- Entrada: SQLite Bronze.
- Saida: schema configurado por `POSTGRES_SCHEMA`, atualmente `dbf_importacao`.
- Regra: COPY binario com `asyncpg`, texto sanitizado contra bytes NUL e validacao de contagem.
- Uso: descoberta de dados, perfilamento e origem dos modelos Gold.
- Restricao: nao e a camada consumida diretamente pelo Metabase em producao.

## Gold: modelo de negocio para o Metabase

- Entrada: tabelas Silver e coletas manuais aprovadas.
- Saida planejada: schema `dw_gold` no PostgreSQL.
- Conteudo esperado: dimensoes conformadas, fatos de atendimento, faturamento, recebimento, estoque e metricas BSC.
- Regra: toda metrica precisa ter formula, origem, competencia, responsavel, baseline, meta e tratamento de excecoes documentados.

## Coleta manual

Metas, baselines, CSAT/NPS, escalas, treinamentos, eventos adversos e planos PDCA nao devem ser estimados a partir dos DBFs. O contrato de coleta esta em `consultoria/COLETA_MANUAL_METRICAS_METABASE.md` e o script de armazenamento em `sql/coleta_manual_metricas.sql`.

## Qualidade e privacidade

- Validar chaves, datas, status, cancelamentos e duplicidades antes de liberar uma fato Gold.
- Restringir Metabase a campos necessarios; evitar expor identificadores pessoais e conteudo clinico.
- Registrar a data da ultima carga e checks de completude em cada dashboard.