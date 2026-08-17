## Why

O fluxo atual de transição do paciente pós-cirúrgico do Bloco Cirúrgico (BC) para a UTI carece de uma comunicação clínica formalizada e de fácil acesso. A equipe da UTI precisa de informações críticas (como instabilidade hemodinâmica, doses de aminas, presença de drenos) antes de autorizar a vinda do paciente para o leito, para que possam preparar a estrutura de suporte necessária. Este projeto visa digitalizar essa "Passagem de Caso" de forma ágil e segura, prevenindo falhas de comunicação sem introduzir cliques burocráticos no fluxo geral de pacientes sem criticidade.

## What Changes

- **No Bloco Cirúrgico:** Ao clicar em "Finalizar Cirurgia" no card de uma solicitação cirúrgica, o usuário será questionado se deseja inserir informações de Passagem de Caso.
  - Se escolher **Não**: A cirurgia é concluída imediatamente (zero cliques extras).
  - Se escolher **Sim**: Um campo de texto expandido é exibido para digitar observações clínicas críticas antes de concluir.
- **Na UTI (Painel de Leitos):** Ao clicar em "Liberar Encaminhamento" para um leito reservado:
  - Se o Bloco Cirúrgico **não** inseriu informações de passagem: A liberação ocorre de forma instantânea em um clique (comportamento atual mantido).
  - Se o Bloco Cirúrgico **inseriu** informações: Abre-se obrigatoriamente um modal com os dados clínicos inseridos. O leito só será liberado fisicamente quando o usuário clicar em "Ciente e Liberar". Ele também pode clicar em "Cancelar" para adiar a liberação se o leito não estiver pronto.
- **Histórico:** As informações da passagem de caso serão mantidas gravadas nos logs da solicitação e leito para fins de auditoria.

## Capabilities

### New Capabilities
- `passagem-caso`: Implementa o fluxo de registro opcional de observações críticas pelo Bloco Cirúrgico e a leitura obrigatória com checkpoint de confirmação pela UTI no ato da liberação do encaminhamento.

### Modified Capabilities
- `solicitacao-leitos`: Atualizado para incluir a interface de questionário de passagem de caso na conclusão cirúrgica.
- `internacao-leitos`: Atualizado para incluir o checkpoint e modal de visualização de passagem de caso na liberação de encaminhamento.

## Impact

- **Banco de Dados (Modelos):** Adição de um campo opcional text/string `passagem_caso` na entidade `SolicitacaoLeito`.
- **API do Backend:**
  - Ajuste no endpoint de conclusão de cirurgia para receber o payload de `passagem_caso`.
  - Ajuste na listagem de leitos para expor o campo `passagem_caso` quando um leito tiver reserva do bloco associada.
- **Frontend (Vue):**
  - Modificação do fluxo de "Finalizar Cirurgia" no painel de solicitações.
  - Modificação do fluxo do botão "Liberar Encaminhamento" no painel de leitos da UTI.
