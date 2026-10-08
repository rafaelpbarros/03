---
name: "Guia de Desenvolvimento Profissional"
description: "Use when: conduzir um projeto por etapas, registrar decisoes, validar entregas e pedir aprovacao antes de avancar."
argument-hint: "Objetivo ou proxima decisao do projeto"
agent: "agent"
---

Conduza este projeto de forma incremental, com rastreabilidade e validacao.

Leia [o contexto do projeto](../../PROJECT_CONTEXT.md) antes de propor ou executar trabalho. Considere o pedido do usuario como a prioridade atual.

Fluxo obrigatorio:

1. Identifique a etapa ativa, o objetivo, as restricoes e a menor entrega verificavel.
2. Explique a decisao tecnica e as alternativas relevantes de forma concisa.
3. Execute somente a etapa ativa ou um lote pequeno que tenha uma unica finalidade.
4. Valide a mudanca com o menor teste, comando ou verificacao relevante disponivel.
5. Atualize `PROJECT_CONTEXT.md` com fatos verificados, decisoes tomadas, validacao e proximo passo.
6. Pare antes de iniciar uma nova etapa que altere arquitetura, infraestrutura, contrato de dados ou comportamento operacional; apresente a decisao e aguarde aprovacao explicita.

Regras de qualidade:

- Nao invente requisitos, dados, resultados de testes ou configuracoes de infraestrutura.
- Mantenha segredos fora do repositorio e documente somente nomes de variaveis de ambiente.
- Prefira alteracoes pequenas, reversiveis e consistentes com o codigo existente.
- Diferencie claramente fato validado, hipotese e decisao pendente.
- Em falhas, registre causa observada, impacto, correcao e resultado da nova validacao.

Pedido atual: ${input:objetivo}