## Why

Atualmente, ao acessar a página de todos os alertas no Modo TV (onde o cabeçalho e barra lateral de navegação comum estão ocultos), não há como retornar à tela de leitos sem usar o botão de "Voltar" do navegador. Além disso, no próprio popover do sininho, os usuários não conseguem arquivar/confirmar individualmente as notificações sem navegar para fora da tela.

## What Changes

- **Botão Voltar na Tela de Alertas (`Alertas.vue`):** Adicionar um botão de navegação "Voltar ao Painel" com ícone de seta apontando para a esquerda para permitir retorno rápido.
- **Ação "Ciente" Direta no Popover (`NotificationsPopover.vue`):** Exibir um pequeno botão "Ciente" ao lado do horário de cada alerta não lido na listagem suspensa para que o operador possa dar ciência e arquivá-lo imediatamente sem sair do painel.

## Capabilities

### New Capabilities

### Modified Capabilities
- `alertas`: Navegabilidade e facilidade de arquivamento das notificações.

## Impact

- **Frontend:** `frontend/src/views/Alertas.vue` e `frontend/src/components/NotificationsPopover.vue`
