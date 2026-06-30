## 1. Estilização Visual

- [x] 1.1 Adicionar a animação customizada `@keyframes pulse-warning` e a classe `.animate-pulse-warning` em `frontend/src/index.css`
- [x] 1.2 Atualizar `frontend/src/components/BedCard.vue` para aplicar condicionalmente a classe `.animate-pulse-warning` quando o leito tiver cirurgia finalizada (`proximoPaciente && cirurgiaFinalizada && !encaminhamentoLiberado`) e o perfil logado for UTI ou Administrador

## 2. Alerta Sonoro e Controle de Áudio

- [x] 2.1 Implementar a função sintetizadora de áudio (beep) usando a API nativa `AudioContext` em `frontend/src/views/Home.vue`
- [x] 2.2 Adicionar um botão discreto de Ativar/Desativar Som ao lado do filtro de leitos no cabeçalho da visão geral em `frontend/src/views/Home.vue`, persistindo o estado no `localStorage` sob a chave `hc_uti_som_alerta`
- [x] 2.3 Implementar lógica de controle de transição no método `loadLeitos` em `frontend/src/views/Home.vue` para manter controle dos leitos que já dispararam o bipe, assegurando que o som seja tocado apenas na transição inicial de uma cirurgia finalizada (evitando bipe contínuo a cada ciclo de polling)

## 3. Validação e Testes

- [x] 3.1 Executar a aplicação e verificar se a animação do card e a emissão do som ocorrem estritamente para usuários pertencentes aos perfis UTI ou Administrador
- [x] 3.2 Testar a funcionalidade de silenciar áudio do painel e confirmar que ela persiste corretamente após a recarga da página
