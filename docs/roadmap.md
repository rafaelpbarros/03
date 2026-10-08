# Roteiro de Entrega

## Concluido

- Extracao DBF para SQLite Bronze.
- Carga SQLite para PostgreSQL Silver.
- PostgreSQL local por Docker Compose.
- Relatorios de execucao e medicao de desempenho.
- Catalogo BSC de metricas e estrutura de coleta manual.
- Fundacao documental e de versionamento.

## Proxima etapa aprovada

Mapear as metricas P0 para tabelas, colunas, chaves, status e datas na Silver. A entrega deve ser um contrato de metricas por indicador, sem criar ainda modelos Gold ou dashboards.

## Etapas posteriores sujeitas a aprovacao

1. Criar dimensoes e fatos Gold no PostgreSQL.
2. Popular e validar Gold contra a Silver.
3. Adicionar Metabase ao Compose e criar as abas por categoria.
4. Adicionar Airflow com banco de metadados dedicado e `LocalExecutor`.
5. Preparar a implantacao Ubuntu, backup e monitoramento.

## Criterios de passagem

- Cada metrica tem formula, baseline, meta, fonte e responsavel aprovados.
- Cada modelo Gold possui validacao de chaves, contagens e dados ausentes.
- Dashboards exibem data da ultima carga e nao expõem dados pessoais desnecessarios.
- Infraestrutura nova possui instrucoes de operacao, recuperacao e segredos externos ao Git.