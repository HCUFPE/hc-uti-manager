## Why

A diferenciação visual e a categorização dos alertas do sistema (crítico, aviso, informativo) trazem complexidade desnecessária para o usuário final, que prefere um fluxo simplificado e homogêneo. Adicionalmente, a exclusão automática de alertas de certas categorias ("Infeccioso", "Permanencia", "Limpeza") durante a sincronização impede a auditoria e a análise histórica completa das ocorrências no leito da UTI.

## What Changes

- **Simplificação Visual dos Alertas**: Unificação do visual de todos os alertas do sistema (críticos, avisos e informativos) sob o mesmo padrão de design, ícone e cor neutra (azul/informativa), tanto na tela de listagem de alertas quanto no popover de notificações rápidas.
- **Prevenção de Exclusão de Alertas**: Desativação completa de qualquer rotina de exclusão automática ou limpeza de alertas no backend durante a sincronização, garantindo que o histórico seja 100% preservado indefinidamente.

## Capabilities

### New Capabilities

<!-- Nenhuma nova capacidade é introduzida neste ciclo -->

### Modified Capabilities

- `alertas`: Unificação visual de todos os alertas no frontend e desativação de remoções/limpezas automatizadas na sincronização de alertas no backend.

## Impact

- **Frontend**: Componentes `frontend/src/views/Alertas.vue` e `frontend/src/components/NotificationsPopover.vue` serão simplificados para mapear todas as severidades para um único estilo visual.
- **Backend**: Método `_sincronizar_alertas` em `src/controllers/alerta_controller.py` será alterado para remover a lógica de limpeza de alertas obsoletos.
