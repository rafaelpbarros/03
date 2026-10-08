# Catalogo de Metricas para DW e Metabase

## Objetivo

Definir a primeira carteira de metricas para o data warehouse (DW) proveniente do ERP FoxPro e para os dashboards Metabase do Hospital Veterinario de Correas.

Este catalogo complementa o BSC da consultoria. Ele prioriza indicadores comuns na gestao de hospitais veterinarios, com enfase em resultado financeiro, experiencia do cliente, produtividade clinica, capacidade operacional e qualidade do dado.

## Como a relevancia foi ranqueada

A classificacao combina cinco criterios, cada um avaliado de 1 a 5:

1. **Impacto estrategico**: aderencia a Missao, Visao, Valores e objetivos BSC.
2. **Impacto economico**: influencia em receita, margem, caixa ou custo.
3. **Acionabilidade**: capacidade de uma area agir ao observar o resultado.
4. **Pratica de mercado**: frequencia em rotinas de gestao de clinicas e hospitais veterinarios.
5. **Viabilidade no ERP**: disponibilidade provavel na base atual, sem nova coleta manual.

O resultado determina a prioridade de implementacao, nao uma meta de desempenho:

| Prioridade | Faixa | Uso recomendado |
| --- | --- | --- |
| P0 | 21 a 25 | Primeiro dashboard executivo e rotina mensal de resultado. |
| P1 | 16 a 20 | Segunda onda, apos validar regras de negocio e historico. |
| P2 | 15 ou menos | Especializado; depende de nova captura, auditoria ou processo. |

## Legenda de disponibilidade

| Situacao | Significado |
| --- | --- |
| Provavel no ERP | Ha dominio fonte identificado; falta validar chaves, status e regra de negocio. |
| Condicional | Dados parecem existir, mas a metrica depende de relacionamento ou campo ainda nao confirmado. |
| Nova captura | Nao deve ser inferida do ERP; exige pesquisa, cadastro de RH, auditoria clinica ou controle de acoes. |

## Financeiro e rentabilidade

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 1 | Receita liquida realizada | P0 | Indicador central de crescimento e base para as demais taxas. | Faturamento valido menos descontos, devolucoes, cancelamentos e tributos definidos. | Provavel no ERP: notas, faturas, recebimentos e devolucoes. |
| 2 | Margem de contribuicao por servico | P0 | Evita crescer receita em atividades que consomem resultado. | Receita liquida do servico menos custo variavel de medicamentos, materiais, exames terceiros e comissoes. | Condicional: itens de nota, estoque, entradas, saidas e repasses. |
| 3 | Contas a receber em aberto e inadimplencia | P0 | Receita faturada nao equivale a caixa; e essencial para previsao financeira. | Titulos vencidos e em aberto dividido pelo total a receber, com aging por faixa de atraso. | Provavel no ERP: faturas, recebimentos, boletos e movimentos bancarios. |
| 4 | Fluxo de caixa realizado e projetado | P0 | Controla liquidez e antecipa necessidade de caixa. | Entradas menos saidas por dia, semana e mes; projetado usa vencimentos futuros. | Provavel no ERP: caixa, banco, recebimentos, pagamentos e faturas. |
| 5 | Crescimento de receita comparavel | P0 | Meta BSC de aumento de receita precisa separar crescimento real de efeito de calendario. | Variacao percentual da receita versus mesmo periodo anterior, com dias abertos equivalentes. | Provavel no ERP: documentos financeiros com data e status. |
| 6 | Ticket medio por atendimento | P0 | Indicador comercial padrao que conecta valor entregue, mix e oportunidade de servico. | Receita liquida dividida por atendimentos ou fichas concluidas. | Condicional: faturamento, itens e ficha/atendimento. |
| 7 | Receita e margem por linha de servico | P1 | Mostra a contribuicao de consulta, cirurgia, exames, internacao, estetica e pet shop. | Receita e margem agrupadas por categoria de servico/produto. | Condicional: itens, servicos, produtos e grupos de estoque. |
| 8 | Desvio de orcamento financeiro | P1 | O BSC pede previsao de receitas e despesas com acuracia. | Realizado menos orcado, em valor e percentual, por conta e centro de resultado. | Nova captura: orcamento aprovado; realizado provavel no ERP. |
| 9 | Taxas financeiras por meio de pagamento | P1 | Cartao e bancos podem reduzir margem sem aparecer na receita bruta. | Taxas e juros divididos pela receita recebida por forma de pagamento. | Condicional: formas de recebimento, movimentos e taxas cadastradas. |

## Clientes, demanda e experiencia

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 10 | Clientes ativos, novos e reativados | P0 | Mede crescimento de base e alcance regional previstos na visao. | Clientes com compra ou atendimento no periodo, primeira ocorrencia e retorno apos inatividade definida. | Provavel no ERP: clientes, animais, atendimentos e faturamento. |
| 11 | Taxa de retencao de clientes | P0 | Meta explicita do BSC e indicador recorrente de saude comercial. | Clientes ativos em dois periodos consecutivos dividido pelos ativos da coorte inicial. | Condicional: identificador estavel de cliente e historico de atendimento/receita. |
| 12 | Taxa de retorno ou recorrencia | P0 | Complementa retencao ao mostrar a frequencia de novas visitas. | Clientes com novo atendimento no periodo dividido pelos clientes elegiveis para retorno. | Condicional: atendimentos por cliente/animal e janela de elegibilidade. |
| 13 | Taxa de faltas e cancelamentos | P0 | Agenda ociosa reduz produtividade, atrasa atendimento e perde receita. | Agendamentos cancelados ou sem comparecimento dividido pelo total agendado. | Condicional: agenda precisa registrar status, data e motivo. |
| 14 | Conversao de orcamento em venda | P1 | Mede aproveitamento comercial sem incentivar procedimentos inadequados. | Orcamentos aprovados ou faturados dividido pelos orcamentos emitidos, por servico e periodo. | Condicional: orcamentos, itens, ficha e notas. |
| 15 | Tempo de espera do cliente | P1 | Meta BSC da recepcao e fator direto de satisfacao. | Inicio do atendimento menos horario agendado ou chegada; usar mediana e percentil 90. | Condicional: timestamps de agenda, chegada e inicio de atendimento. |
| 16 | Satisfacao do cliente (CSAT) e NPS | P1 | A visao requer alta satisfacao; receita nao substitui percepcao do tutor. | CSAT: respostas positivas dividido pelo total; NPS: promotores menos detratores. | Nova captura: pesquisa pos-atendimento vinculada a atendimento e canal. |
| 17 | Origem do cliente e custo de aquisicao | P2 | Permite comparar canais e parcerias, especialmente para crescimento regional. | Novos clientes por origem e investimento de marketing dividido por novos clientes. | Nova captura: origem padronizada e investimento por campanha. |

## Operacao clinica e capacidade

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 18 | Volume de atendimentos, procedimentos, exames e cirurgias | P0 | E a base de capacidade, demanda e desempenho por area. | Quantidade concluida por dia, especialidade, profissional e tipo de servico. | Provavel no ERP: fichas, itens, servicos, exames e cirurgias. |
| 19 | Conversao de consulta em cirurgia | P0 | Meta BSC explicita; deve ser acompanhada com criterio clinico e auditoria. | Cirurgias elegiveis vinculadas a consultas divididas por consultas elegiveis. | Condicional: vinculo entre ficha, indicacao e cirurgia. |
| 20 | Receita e producao por profissional | P0 | Conecta capacidade, especialidade e planejamento de escala. | Receita, consultas, procedimentos e exames por profissional, ajustados por horas disponiveis. | Condicional: medico/profissional responsavel e escala de trabalho. |
| 21 | Ocupacao, giro e permanencia da internacao | P1 | Indicadores padrao para gerir leitos, equipe e experiencia do paciente. | Leitos-dia ocupados dividido por leitos-dia disponiveis; altas por leito; dias entre admissao e alta. | Condicional: ficha de internacao, canil/leito, admissao e alta. |
| 22 | Taxa de recuperacao e readmissao | P1 | Complementa a meta BSC de recuperacao com resultado e continuidade assistencial. | Altas com desfecho definido; readmissoes na janela clinica aprovada. | Nova captura ou auditoria: desfecho clinico padronizado e regra de readmissao. |
| 23 | Tempo de ciclo do atendimento | P1 | Reduzir tempo medio exige decompor recepcao, espera, consulta, exame e fechamento. | Horas ou minutos entre chegada, inicio e encerramento, por etapa. | Condicional: eventos com data/hora confiaveis. |
| 24 | Retrabalho e nao conformidades | P1 | Meta BSC explicita; mede eficiencia e qualidade de processo. | Atividades refeitas ou nao conformes dividido por atividades concluídas. | Nova captura ou configuracao: registro padronizado de evento, causa e impacto. |
| 25 | Eventos adversos por 100 procedimentos | P2 | Permite qualidade clinica comparavel sem usar apenas contagens absolutas. | Eventos classificados dividido pelos procedimentos elegiveis vezes 100. | Nova captura: taxonomia, severidade, revisao clinica e denominador. |

## Estoque, medicamentos e suprimentos

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 26 | Ruptura de estoque | P0 | Falta de medicamento ou material afeta atendimento, receita e seguranca. | Itens com saldo abaixo do minimo dividido pelos itens ativos, com dias em ruptura. | Condicional: saldo, minimo, movimentacao e item ativo. |
| 27 | Giro e cobertura de estoque | P1 | Equilibra capital imobilizado, perda e disponibilidade. | Custo consumido dividido pelo estoque medio; dias de cobertura pelo consumo medio. | Condicional: entradas, saidas, custo e saldo historico. |
| 28 | Perdas por vencimento, avaria e devolucao | P1 | Reduz custo evitavel e melhora qualidade do abastecimento. | Valor e quantidade descartados ou devolvidos por motivo, dividido pelas compras ou consumo. | Condicional: lote, validade e motivo de baixa. |
| 29 | Margem por medicamento e produto | P1 | Medicamentos e produtos podem gerar receita com margem muito distinta. | Receita liquida do item menos custo de aquisicao e taxas variaveis. | Condicional: itens de venda, entrada e criterio de custo aprovado. |

## Pessoas, desenvolvimento e lideranca

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 30 | Produtividade por hora disponivel | P1 | Evita comparar profissionais apenas por volume sem considerar jornada e funcao. | Atendimentos, procedimentos ou receita divididos por horas efetivamente disponiveis. | Nova captura: escala, jornada e classificacao de funcao. |
| 31 | Turnover e retencao de novos colaboradores | P1 | Meta BSC explicita e indicador de continuidade operacional. | Desligamentos e permanencia apos 12 meses, por area e motivo. | Nova captura ou integracao de RH. |
| 32 | Horas de treinamento e cobertura de capacitação | P1 | Meta BSC explicita; deve ser ligada a competencias e nao apenas presenca. | Horas concluídas por pessoa e percentual da equipe treinada no tema definido. | Nova captura: trilha, presenca, carga horaria e avaliacao. |
| 33 | Clima, engajamento e avaliacao de lideranca | P2 | Sustenta a visao de equipe preparada e a meta de lideranca. | Pontuacao de pesquisa anonima por dimensao, com minimo de respostas. | Nova captura: pesquisa anonima e cadastro de equipe. |

## Governanca BSC, PDCA e qualidade do DW

| Rank | Metrica | Prioridade | Por que e relevante | Definicao inicial | Disponibilidade e dominios candidatos |
| --- | --- | --- | --- | --- | --- |
| 34 | Atingimento das metas BSC | P0 | E a pagina executiva que conecta operacao, clientes, pessoas e financeiro. | Indicadores dentro da meta dividido pelo total aplicavel, ponderado pela prioridade estrategica. | Condicional: catalogo de metas, formulas, competencia e responsavel. |
| 35 | Gap para a meta e tendencia de fechamento | P0 | O PDCA requer enxergar distancia, velocidade e prazo de correcao. | Meta menos realizado, tendencia recente e previsao de atingimento. | Condicional: serie historica, baseline e regra de tendencia. |
| 36 | Planos de acao PDCA no prazo | P1 | Fecha o ciclo entre detectar desvio e executar melhoria. | Acoes concluídas no prazo dividido pelas acoes vencidas ou previstas. | Nova captura: backlog com responsavel, prazo, causa e evidencia. |
| 37 | Atualidade e completude dos dados | P0 | Sem confianca na carga, o dashboard pode induzir decisoes erradas. | Tempo desde a ultima carga; registros obrigatorios preenchidos; chaves orfas e duplicidades. | Provavel no DW: log de carga, testes e dimensoes conformadas. |
| 38 | Conciliacao entre faturamento, recebimento e banco | P1 | Detecta diferencas financeiras antes de uma reuniao de resultado. | Diferenca entre documentos emitidos, baixas financeiras e movimentos bancarios, por competencia. | Condicional: regras de conciliacao e chaves de origem. |

## Primeiro dashboard recomendado

O primeiro ciclo deve conter somente metricas P0 com regras fechadas. A ordem de implementacao recomendada e:

1. **Pagina executiva BSC**: receita liquida, crescimento, margem de contribuicao, inadimplencia, clientes ativos, retencao, volume assistencial, conversao consulta-cirurgia, ruptura de estoque, atingimento de metas e atualidade da carga.
2. **Pagina financeira**: receita, margem, recebiveis, caixa, ticket e detalhamento por linha de servico.
3. **Pagina clientes e comercial**: novos clientes, retencao, retorno, faltas, agenda e conversao de orcamento.
4. **Pagina operacao**: producao por area e profissional, cirurgia, exames, internacao e estoque critico.
5. **Pagina de confianca e PDCA**: qualidade dos dados, gaps de meta e planos de acao quando o registro for implantado.

## Regras obrigatorias antes de publicar uma metrica

Cada metrica do DW deve possuir um registro no catalogo tecnico com:

- nome de negocio e codigo estavel;
- objetivo BSC e categoria;
- formula, unidade, polaridade e granularidade;
- baseline, meta, periodo de competencia e versao da meta;
- dimensoes de analise permitidas;
- tabelas, campos e regra de transformacao no DW;
- responsavel de negocio e responsavel tecnico;
- periodicidade de atualizacao;
- tratamento de cancelamentos, estornos, devolucoes, duplicidades e dados ausentes;
- status de qualidade e data da ultima validacao.

## Limites e proximas decisoes

- O ERP parece suportar a maior parte das metricas P0 financeiras, comerciais, de producao e estoque, mas a modelagem fisica ainda precisa confirmar chaves, datas e status.
- CSAT/NPS, clima, treinamento, escalas, eventos adversos, desfecho clinico e planos de acao PDCA nao devem ser estimados a partir do DBF. Eles exigem nova captura ou integracao formal.
- Metas descritas nos documentos de consultoria devem ser revalidadas com data inicial, baseline e responsavel antes de serem exibidas como compromisso atual.
- O DW deve usar identificadores tecnicos e expor no Metabase apenas o menor conjunto necessario de dados pessoais e clinicos.

## Referencias de priorizacao

- Material interno: `H. Petropolis - Balance Scorecard - BSC v.02 .pdf`, `Indicadores e Ciclo PDCA.pdf` e `Missão Visão e Valores_v.03.pdf`.
- Kaplan, R. S. e Norton, D. P.: Balanced Scorecard e mapas estrategicos, para equilibrio entre perspectivas financeira e nao financeira.
- Praticas recorrentes de gestao veterinaria: acompanhamento de receita, ticket medio, clientes ativos e recorrentes, producao por profissional, mix de servicos, recebiveis, estoque e capacidade assistencial.

> Este documento e um catalogo de requisitos. Nenhuma metrica deve ser considerada implementada ou validada ate que sua regra de negocio e seu mapeamento para o DW sejam aprovados.