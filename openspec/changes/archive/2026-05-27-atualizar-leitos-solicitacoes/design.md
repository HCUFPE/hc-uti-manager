## Context

Atualmente, o censo e a fila de leitos do AGHU são atualizados em segundo plano a cada 2 minutos pelo layout principal (`DefaultLayout.vue`) através do endpoint `/api/alertas/gerar`. No entanto, as telas específicas de Leitos (`Home.vue`) e de Solicitações (`Solicitacoes.vue`) não possuem um mecanismo de polling correspondente para re-renderizar a tela automaticamente ao obter novos dados, obrigando o usuário a recarregar manualmente a página ou a interagir com algum botão de ação para ver as atualizações.

## Goals / Non-Goals

**Goals:**
- Implementar polling a cada 2 minutos (120.000 ms) em `Home.vue` para chamar `loadLeitos()`.
- Implementar polling a cada 2 minutos (120.000 ms) em `Solicitacoes.vue` para chamar `carregarSolicitacoes()`.
- Garantir a limpeza adequada de todos os temporizadores via `onUnmounted` para prevenir vazamentos de memória na Single Page Application (SPA).

**Non-Goals:**
- Não iremos alterar endpoints do backend.
- Não iremos configurar web sockets ou server-sent events (SSE).
- Não adicionaremos polling em outras telas menores como Histórico ou Indicadores, a menos que solicitado.

## Decisions

### Decision 1: Polling Local via setInterval no Frontend
- **Opção A:** Utilizar `setInterval` local em cada view (`Home.vue` e `Solicitacoes.vue`) sincronizado com o tempo de 2 minutos.
- **Opção B:** Utilizar um Store global do Pinia para gerenciar o estado global de leitos e fazer polling centralizado.
- **Escolha:** Opção A. A Opção A é simples, direta e isola a responsabilidade de atualização automática apenas às telas onde os usuários ficam ativamente monitorando em tempo real. Além disso, garante que o polling só ocorra enquanto a tela estiver visível e ativa.

## Risks / Trade-offs

- **[Risco] Vazamento de Memória (Memory Leaks)** → Se o timer não for cancelado, a SPA continuará chamando a API mesmo após mudar de tela.
  - **Mitigação:** Importar e registrar `onUnmounted` do Vue em ambos os arquivos, limpando o respectivo `IntervalId` com `clearInterval()`.
- **[Risco] Sobrecarga do Banco de Dados** → Múltiplos usuários com abas abertas gerando chamadas concorrentes à API.
  - **Mitigação:** Manter o intervalo em 2 minutos (120.000 ms), que é o mesmo intervalo já consolidado no `DefaultLayout.vue` para alertas de segundo plano.
