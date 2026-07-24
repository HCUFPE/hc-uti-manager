## Context

As solicitações concluídas atualmente são renderizadas em uma grid aberta de duas colunas abaixo das seções de solicitações pendentes e reservadas. Não há indicador de data/hora de conclusão, apenas uma indicação textual "Sincronizado com AGHU".

## Goals / Non-Goals

**Goals:**
- Colapsar a seção de solicitações concluídas por padrão.
- Adicionar controle interativo para expandir/recolher a seção.
- Exibir a data/hora de conclusão (`atualizado_em`) formatada em cada card.

**Non-Goals:**
- Não ocultar as solicitações pendentes ou reservadas (estas devem continuar abertas por padrão).

## Decisions

### Estado do Collapse no Frontend
Utilizar uma variável reativa local no Vue (`const concluidaExpandida = ref(false)`) para controlar a visibilidade da grid de solicitações concluídas.
- *Alternativa considerada:* Persistir o estado de expandido no localStorage. Rejeitado por simplicidade de implementação (sempre começar fechado ao recarregar a página é o comportamento padrão desejado).

### Data de Conclusão via campo `atualizado_em` do Backend
Mapear o campo `atualizado_em` na controller `SolicitacaoLeitoController.listar_solicitacoes` do backend (formatando como string BR `DD/MM/AAAA HH:MM`) e expor para o frontend na resposta da listagem de solicitações.
- *Alternativa considerada:* Criar uma coluna nova no banco local dedicada chamada `concluida_em`. Rejeitado, pois no fluxo da aplicação o status "Concluída" é um estado terminal e o campo `atualizado_em` já registra com precisão a data/hora em que a última alteração de status ocorreu.

## Risks / Trade-offs

Nenhum risco significativo identificado. O impacto de performance e layout é insignificante.
