# Coleta Manual de Metricas para o Metabase

## Finalidade

Este documento lista as informacoes que nao devem ser inferidas dos DBFs atuais. Elas serao registradas por competencia no DW para complementar as metricas automaticas do ERP.

As abas sugeridas abaixo sao paginas de navegacao no Metabase. Elas nao exigem uma tabela por aba: todas as entradas manuais usam a mesma tabela historica e sao filtradas pela categoria.

## Regra de preenchimento

- Registrar uma linha para cada valor, periodo e recorte relevante.
- Usar o primeiro dia do mes como `periodo_inicio` para metricas mensais.
- Registrar a fonte e uma evidencia curta em `observacao`.
- Nao registrar nomes de pacientes, tutores ou informacoes clinicas identificaveis.
- Corrigir um valor criando nova versao da coleta; nao apagar o historico.
- Atualizar metas, baselines e responsaveis antes de divulgar qualquer semaforo no Metabase.

## Aba 1: Financeiro e rentabilidade

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `meta_receita_liquida` | Meta de receita liquida | Meta mensal aprovada, baseline e data de vigencia. | Mensal ou quando revisada. | Obrigatoria para BSC. |
| `meta_margem_contribuicao` | Meta de margem de contribuicao | Meta percentual ou em R$, por hospital e linha de servico quando aplicavel. | Mensal ou trimestral. | Obrigatoria para BSC. |
| `custo_variavel_servico` | Custo variavel por servico | Materiais, medicamentos, exames terceiros, comissoes e outros custos diretamente atribuidos. | Mensal. | Necessaria para margem por servico. |
| `orcamento_receita` | Orcamento de receita | Valor orcado por mes, conta ou linha de servico. | Anual, revisado mensalmente. | Necessaria para desvio orcamentario. |
| `orcamento_despesa` | Orcamento de despesa | Valor orcado por mes e conta gerencial. | Anual, revisado mensalmente. | Necessaria para desvio orcamentario. |
| `saldo_caixa_manual` | Saldo de caixa validado | Saldo inicial e final conciliado quando banco/caixa nao estiver confiavel no ERP. | Diario ou semanal. | Temporaria, ate a conciliacao automatica. |
| `meta_inadimplencia` | Meta de inadimplencia | Limite percentual e criterio de atraso aprovado. | Mensal ou quando revisada. | Obrigatoria para BSC. |

## Aba 2: Clientes e comercial

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `meta_clientes_ativos` | Meta de clientes ativos | Meta mensal e regra aprovada de cliente ativo. | Mensal ou quando revisada. | Obrigatoria para BSC. |
| `meta_retencao_clientes` | Meta de retencao | Meta percentual, janela de comparacao e coorte elegivel. | Mensal ou trimestral. | Obrigatoria para BSC. |
| `agenda_faltas` | Faltas em agenda | Numero de faltas, periodo, unidade, especialidade e motivo padronizado. | Diario, consolidado mensalmente. | Necessaria: `STATUS` da agenda esta vazio. |
| `agenda_cancelamentos` | Cancelamentos em agenda | Numero de cancelamentos e motivo padronizado. | Diario, consolidado mensalmente. | Necessaria: `STATUS` da agenda esta vazio. |
| `csat_respondentes` | Pesquisa de satisfacao | Total de respostas e total de respostas satisfeitas; informar canal da pesquisa. | Mensal. | Necessaria para CSAT. |
| `nps_promotores` | Pesquisa NPS: promotores | Quantidade de notas 9 e 10. | Mensal. | Necessaria para NPS. |
| `nps_neutros` | Pesquisa NPS: neutros | Quantidade de notas 7 e 8. | Mensal. | Necessaria para NPS. |
| `nps_detratores` | Pesquisa NPS: detratores | Quantidade de notas de 0 a 6. | Mensal. | Necessaria para NPS. |
| `tempo_espera_minutos` | Tempo de espera | Media e percentil 90, em minutos, por unidade ou especialidade. | Semanal, consolidado mensalmente. | Necessaria enquanto nao houver timestamps confiaveis. |
| `origem_novos_clientes` | Origem de novos clientes | Quantidade por canal padronizado: indicacao, Google, redes sociais, parceiro, passagem e outros. | Mensal. | Recomendado para crescimento regional. |
| `investimento_marketing` | Investimento de marketing | Valor por canal e campanha. | Mensal. | Necessaria para custo de aquisicao. |

## Aba 3: Operacao clinica e capacidade

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `meta_volume_atendimentos` | Meta de volume | Meta mensal de atendimentos, procedimentos, exames e cirurgias. | Mensal ou quando revisada. | Obrigatoria para BSC. |
| `meta_conversao_cirurgia` | Meta de conversao consulta-cirurgia | Meta percentual e definicao de consulta/cirurgia elegivel. | Mensal ou quando revisada. | Obrigatoria para BSC. |
| `cirurgias_indicadas` | Cirurgias indicadas elegiveis | Quantidade de indicacoes clinicamente elegiveis para conversao. | Mensal. | Necessaria se o vinculo nao existir no ERP. |
| `leitos_disponiveis` | Capacidade de internacao | Numero de leitos ou canis ativos por dia e unidade. | Quando houver alteracao; consolidado mensalmente. | Necessaria para taxa de ocupacao. |
| `admissoes_internacao` | Admissoes de internacao | Quantidade de internacoes por periodo, quando nao estiver integralmente identificavel. | Diario, consolidado mensalmente. | Condicional. |
| `altas_recuperadas` | Altas com recuperacao | Quantidade de altas classificadas como recuperadas segundo protocolo clinico aprovado. | Mensal. | Necessaria para taxa de recuperacao. |
| `readmissoes` | Readmissoes | Quantidade de readmissoes na janela clinica definida. | Mensal. | Necessaria para qualidade assistencial. |
| `retrabalho_operacional` | Retrabalho | Quantidade de atividades refeitas, area, motivo e impacto estimado. | Semanal, consolidado mensalmente. | Necessaria: exige classificacao de evento. |
| `nao_conformidades` | Nao conformidades | Quantidade, categoria, severidade e situacao de tratamento. | Semanal, consolidado mensalmente. | Necessaria para qualidade de processo. |
| `eventos_adversos` | Eventos adversos | Quantidade, tipo, severidade e procedimento relacionado, sem dados identificaveis. | Mensal. | Necessaria para qualidade clinica. |

## Aba 4: Estoque e suprimentos

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `estoque_minimo_item` | Estoque minimo | Codigo do item, unidade, estoque minimo e ponto de reposicao. | Na inclusao ou revisao de item. | Necessaria para ruptura automatica. |
| `estoque_perda_vencimento` | Perda por vencimento | Quantidade e valor descartados por vencimento. | Mensal. | Condicional: validar motivo de baixa no ERP. |
| `estoque_perda_avaria` | Perda por avaria | Quantidade e valor descartados por avaria. | Mensal. | Condicional: validar motivo de baixa no ERP. |
| `estoque_perda_outros` | Outras perdas | Quantidade, valor e motivo padronizado. | Mensal. | Condicional: validar motivo de baixa no ERP. |
| `meta_ruptura_estoque` | Meta de ruptura | Limite maximo de itens ou dias em ruptura. | Mensal ou quando revisada. | Obrigatoria para BSC. |

## Aba 5: Pessoas e desenvolvimento

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `horas_disponiveis_profissional` | Horas disponiveis | Horas de escala por profissional, funcao e unidade. | Mensal. | Necessaria para produtividade por hora. |
| `admissoes_colaboradores` | Admissoes | Quantidade por area e tipo de contrato. | Mensal. | Necessaria para turnover. |
| `desligamentos_colaboradores` | Desligamentos | Quantidade por area e motivo agrupado. | Mensal. | Necessaria para turnover. |
| `headcount_final` | Quadro final | Quantidade de colaboradores ativos por area ao fim do mes. | Mensal. | Necessaria para turnover. |
| `horas_treinamento` | Horas de treinamento | Horas concluidas, tema e numero de participantes. | Mensal. | Meta BSC explicita. |
| `colaboradores_treinados` | Cobertura de treinamento | Participantes concluintes por trilha e area. | Mensal. | Complementa horas de treinamento. |
| `clima_respondentes` | Pesquisa de clima | Total de respostas e respostas favoraveis por dimensao. | Trimestral ou semestral. | Necessaria para clima/engajamento. |
| `lideranca_respondentes` | Avaliacao de lideranca | Total de respostas e respostas favoraveis por lideranca/dimensao. | Trimestral ou semestral. | Necessaria para meta de lideranca. |

## Aba 6: BSC, PDCA e qualidade do dado

| Codigo | Metrica ou informacao manual | O que coletar | Frequencia | Necessidade |
| --- | --- | --- | --- | --- |
| `baseline_metrica` | Baseline | Valor de partida, periodo de referencia e metodo usado para cada KPI BSC. | Uma vez e em cada redefinicao. | Obrigatoria para medir evolucao. |
| `meta_metrica` | Meta BSC | Valor-alvo, unidade, vigencia, polaridade, responsavel e peso da metrica. | Quando aprovada ou revisada. | Obrigatoria para semaforo BSC. |
| `acao_pdca_planejada` | Plano PDCA | Quantidade de acoes planejadas, responsavel, prazo e causa raiz resumida. | Semanal. | Necessaria para acompanhar execucao. |
| `acao_pdca_concluida` | Plano PDCA | Quantidade de acoes concluidas, data e evidencia resumida. | Semanal. | Necessaria para medir prazo. |
| `acao_pdca_atrasada` | Plano PDCA | Quantidade de acoes em atraso e impedimento principal. | Semanal. | Necessaria para escalonamento. |
| `qualidade_dado_origem` | Qualidade da fonte | Registros incompletos, duplicados ou sem chave por dominio. | A cada carga. | Pode ser automatizada no DW depois da primeira implementacao. |

## Prioridade de preenchimento

Preencher primeiro, antes do primeiro dashboard executivo:

1. `baseline_metrica` e `meta_metrica` para todas as metricas P0.
2. `custo_variavel_servico`, `orcamento_receita` e `orcamento_despesa`.
3. `agenda_faltas` e `agenda_cancelamentos`.
4. `estoque_minimo_item`.
5. `horas_disponiveis_profissional`.

CSAT/NPS, qualidade clinica, clima e PDCA podem entrar na segunda publicacao, desde que a fonte e o responsavel por cada rotina estejam definidos.

## Uso no Metabase

Criar uma aba por categoria, conforme as seis secoes deste documento. Em todas as abas, aplicar filtros globais de periodo, unidade, area e profissional quando aplicavel.

Nao usar entradas manuais como substitutas permanentes de dados que o ERP pode registrar. Cada coleta manual deve ter dono, frequencia e plano para eventual automacao.