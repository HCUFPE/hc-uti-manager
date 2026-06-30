## Why

Melhorar a velocidade de atendimento e a percepção visual/auditiva da equipe da UTI quando o Bloco Cirúrgico sinalizar que uma cirurgia foi finalizada. Atualmente, o card do leito com cirurgia concluída muda para a cor amarela no painel, mas isso pode passar despercebido. A introdução de uma animação piscante e um sinal sonoro focado exclusivamente na UTI visa acelerar o encaminhamento do paciente para o leito.

## What Changes

- **Alerta Sonoro**: Reproduzir um aviso sonoro (beep/alerta curto) quando um leito mudar para o estado de "Cirurgia Finalizada", garantindo compatibilidade com políticas de autoplay dos navegadores.
- **Destaque Visual Piscante (Flashing)**: Adicionar animação intermitente (piscar) na borda ou fundo do card do leito com cirurgia finalizada.
- **Restrição de Acesso**: Ambas as melhorias (som e animação intermitente) devem ser ativadas apenas para usuários logados com perfil da UTI (ou administradores).
- **Controle de Som**: Adicionar um botão discreto de ligar/desligar som no cabeçalho do Painel de Leitos para permitir que o usuário ative/desative os alertas sonoros.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `internacao-leitos`: Modificar o requisito de "Atualização Visual e Liberação de Encaminhamento pela UTI" para incluir comportamento piscante no card e emissão de alerta sonoro para o perfil UTI.

## Impact

- **Frontend (`frontend/src/components/BedCard.vue`)**: Implementar a classe CSS de animação de piscar condicional ao perfil da UTI e ao status de "Cirurgia Finalizada".
- **Frontend (`frontend/src/views/Home.vue` ou `App.vue`)**: Gerenciar o estado do áudio, carregar o arquivo de áudio e escutar mudanças nas solicitações/leitos para acionar o som para o perfil UTI.
- **Frontend Assets**: Adicionar um arquivo de áudio leve de notificação (ex: em `frontend/public/notification.mp3`).
