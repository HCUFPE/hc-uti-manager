## Context

O alerta sonoro periódico para o NIR foi inicialmente implementado apenas no componente `Home.vue`. Isso significa que, se o usuário do NIR navegar para outra página do sistema, o timer e a reprodução de áudio deixam de funcionar. Para garantir que os operadores do NIR ouçam os alertas até que marquem a notificação como visualizada (ciência dada), precisamos centralizar a lógica no layout global do frontend (`DefaultLayout.vue`) e usar uma gerência de estado centralizada (`uiStore`) para as preferências de áudio (mudo/ativo).

## Goals / Non-Goals

**Goals:**
- Centralizar o controle de áudio (Web Audio API) e a preferência de silenciamento (`isMuted`) na `uiStore` baseada em Pinia.
- Mover a execução periódica do alerta de notificações não lidas (a cada 30 segundos) para o layout global `DefaultLayout.vue`.
- Permitir que o som toque em qualquer tela sob o `DefaultLayout.vue` para usuários NIR (e UTI para alertas normais).
- Adicionar um botão de mute/unmute visual no header do `DefaultLayout.vue` para controle fácil.

**Non-Goals:**
- Não iremos alterar o backend ou as rotas de API existentes de alertas.
- A verificação de leitos e cirurgias concluídas/pendentes continuará restrita à tela `Home.vue`, mas ela invocará o método global exposto pela `uiStore` para tocar o som de cirurgias concluídas.

## Decisions

1. **Centralizar áudio no `uiStore` (`frontend/src/stores/ui.ts`):**
   - Rationale: Centralizar a reprodução sonora no store Pinia evita duplicação de código de oscilador de áudio entre `Home.vue` e `DefaultLayout.vue` e centraliza o controle de volume/mudo.
   
2. **Timer de Notificações no `DefaultLayout.vue`:**
   - Rationale: O layout engloba todas as telas autenticadas do sistema. Centralizar o timer de 30 segundos para notificações não lidas no layout garante que a notificação sonora rode ininterruptamente.

3. **Botão de Controle de Som no Header:**
   - Rationale: Ao tornar o alerta global, o usuário precisa de um atalho visual acessível em qualquer tela para silenciar temporariamente os bipes caso esteja em uma chamada ou atendimento.

## Risks / Trade-offs

- **Bloqueio de Autoplay do Navegador:**
  - *Risco:* Navegadores modernos bloqueiam reprodução de áudio automática antes de qualquer interação do usuário com a página.
  - *Mitigação:* Exibir mensagem amigável ou aproveitar a primeira interação de clique do login para inicializar o AudioContext.
