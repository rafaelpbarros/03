-- Contrato de coleta manual para complementar as metricas do DW.
-- Execute somente apos criar o banco/schema Gold. O script e idempotente.

CREATE SCHEMA IF NOT EXISTS dw_gold;

CREATE TABLE IF NOT EXISTS dw_gold.coleta_manual_metrica (
    coleta_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_metrica TEXT NOT NULL,
    categoria TEXT NOT NULL,
    tipo_medicao TEXT NOT NULL CHECK (
        tipo_medicao IN ('realizado', 'meta', 'baseline', 'numerador', 'denominador')
    ),
    periodo_inicio DATE NOT NULL,
    periodo_fim DATE NOT NULL,
    unidade_negocio TEXT,
    area TEXT,
    profissional_codigo TEXT,
    dimensoes JSONB NOT NULL DEFAULT '{}'::JSONB,
    valor NUMERIC(18, 4) NOT NULL,
    unidade_medida TEXT NOT NULL,
    fonte TEXT NOT NULL,
    observacao TEXT,
    evidenciado_em TIMESTAMPTZ,
    registrado_por TEXT NOT NULL,
    registrado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    versao SMALLINT NOT NULL DEFAULT 1 CHECK (versao > 0),
    CHECK (periodo_fim >= periodo_inicio)
);

CREATE INDEX IF NOT EXISTS ix_coleta_manual_metrica_periodo
    ON dw_gold.coleta_manual_metrica (codigo_metrica, periodo_inicio, periodo_fim);

CREATE INDEX IF NOT EXISTS ix_coleta_manual_metrica_categoria_periodo
    ON dw_gold.coleta_manual_metrica (categoria, periodo_inicio);

CREATE OR REPLACE VIEW dw_gold.v_coleta_manual_metabase AS
SELECT
    categoria,
    codigo_metrica,
    tipo_medicao,
    periodo_inicio,
    periodo_fim,
    unidade_negocio,
    area,
    profissional_codigo,
    dimensoes,
    valor,
    unidade_medida,
    fonte,
    observacao,
    evidenciado_em,
    registrado_por,
    registrado_em,
    versao
FROM dw_gold.coleta_manual_metrica;

-- Modelo de insercao mensal. Copie, remova os comentarios e substitua todos os valores.
-- Nunca execute um valor de exemplo ou uma meta ainda nao aprovada.
-- Para corrigir uma medicao, insira nova linha com versao maior; nao atualize o historico.
-- INSERT INTO dw_gold.coleta_manual_metrica (
--     codigo_metrica, categoria, tipo_medicao, periodo_inicio, periodo_fim,
--     unidade_negocio, area, dimensoes, valor, unidade_medida, fonte,
--     observacao, evidenciado_em, registrado_por, versao
-- ) VALUES (
--     'meta_receita_liquida', 'Financeiro e rentabilidade', 'meta',
--     DATE 'AAAA-MM-01', DATE 'AAAA-MM-DD', 'Unidade de negocio', 'Financeiro',
--     '{"moeda":"BRL"}'::JSONB, <valor_aprovado>, 'BRL',
--     'Documento ou sistema de origem', 'Contexto da medicao', NULL,
--     'identificador_do_responsavel', 1
-- );

-- Consulta que alimenta abas do Metabase. Configure filtros de periodo e categoria na interface.
SELECT
    categoria,
    codigo_metrica,
    tipo_medicao,
    periodo_inicio,
    periodo_fim,
    unidade_negocio,
    area,
    profissional_codigo,
    valor,
    unidade_medida,
    dimensoes,
    fonte,
    observacao,
    evidenciado_em,
    registrado_por,
    registrado_em,
    versao
FROM dw_gold.v_coleta_manual_metabase
ORDER BY categoria, codigo_metrica, periodo_inicio, versao;