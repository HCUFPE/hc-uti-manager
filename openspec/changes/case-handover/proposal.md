## Why

O fluxo de transição do paciente do Bloco Cirúrgico para a UTI necessita de uma passagem de caso clínica estruturada para assegurar que informações críticas (via aérea, suporte ventilatório, acessos e estabilidade hemodinâmica) sejam transmitidas com segurança. Para elevar a segurança do paciente e guiar a equipe cirúrgica em um checklist de transição estruturado, a passagem de caso está sendo implantada como um formulário estruturado com opções de marcação e validações obrigatórias com base no documento oficial do hospital.

## What Changes

- **Formulário Estruturado de Passagem de Caso:** Implantação de campos estruturados e obrigatórios no Bloco Cirúrgico ao finalizar cirurgia:
  - **Identificação Básica:** Procedimento realizado (campo aberto, opcional apenas se "Cirurgia não realizada" for marcada), Anestesia (campo aberto), Alergias (Não / Sim com campo de texto - seleção obrigatória sem valor padrão), Isolamento (Não / Contato / Gotículas / Aerossóis - lista de seleção obrigatória sem valor padrão).
  - **Respiratório (Obrigatório):** Seleção obrigatória de ao menos um item de *Via aérea* (Espontânea, TOT, Traqueostomia, Outro com campo aberto) E ao menos um item de *Suporte* (Ar ambiente, O2 cateter, Máscara, Ventilação mecânica).
  - **Cardiovascular/Hemodinâmico (Obrigatório):** Seleção obrigatória em cada um dos sub-blocos:
    - Hemodinâmica (Estável / Instável)
    - Drogas vasoativas (Não / Sim com texto de droga/vazão)
    - Necessidade de reposição volêmica (Não / Sim)
    - Transfusão (Não / Sim com texto de hemocomponente/quantidade)
  - **Sangramento e Balanço (Obrigatório):** Seleção de uma opção de Sangramento estimado (Mínimo, Pequeno, Moderado, Importante com campo para mL, Não se aplica) E digitação da Diurese intraoperatória (com opção "Não se aplica").
  - **Acessos, dispositivos e feridas (Obrigatório):**
    - Acessos venosos: Periférico (local e data de criação opcional), CVC (local e data de criação opcional), PICC (local e data de criação opcional), Outro (qual, local e data de criação opcional). Remoção da opção "Não se aplica" e obrigatoriedade de selecionar pelo menos um acesso venoso e preencher seu respectivo local.
    - PAI (Não / Sim com local).
    - Sonda vesical (Não / Sim com Nº).
    - Ferida operatória (Local ou a opção "Não se aplica", Obrigatório marcar).
    - Drenos (Não / Sim com tipo/local).
    - Outros (SNG/SNE, Ostomia, Outro) (Preenchimento opcional).
  - **Medicamentos e intercorrências:**
    - Antibiótico (Não / Sim com qual/horário).
    - Outras medicações relevantes (campo aberto).
    - Intercorrências durante o ato (Checklist com "Não houve", "Hipotensão", "Hipertensão", "Arritmia", "Dessaturação", "Broncoespasmo", "Sangramento importante", "Reação medicamentosa", "Parada cardiorrespiratória", "Difícil via aérea", "Outro" com campo de texto).
    - Descrição da intercorrência/conduta (campo de texto, não obrigatório).
  - **Profissional responsável pela passagem** (campo de texto, de preenchimento obrigatório).
- **Edição no Bloco Cirúrgico:** Permitir que o Bloco Cirúrgico edite as informações da passagem de caso enviadas enquanto a UTI ainda não tiver validado a liberação do leito (mesmo que a UTI já tenha clicado em liberar mas não tenha salvo a confirmação definitiva).
- **Visualização Histórica e Concorrência Atômica:** 
  - Controle de concorrência atômica via base de dados (`UPDATE ... WHERE encaminhamento_liberado = False/None`) para evitar condições de corrida em cliques paralelos e duplicidade de logs.
  - Disponibilização do botão **"Ver Passagem"** diretamente na tela de Histórico de Ações (Auditoria), permitindo consultar a ficha clínica retrospectiva a qualquer momento. Para registros antigos anteriores à implantação que não possuem dados de passagem, o sistema trata de forma elegante e exibe "Passagem de caso não cadastrada." no modal.

## Capabilities

### New Capabilities
- `passagem-caso`: Implementa o novo formulário estruturado e regras de obrigatoriedade clínica no ato da finalização de cirurgia e na visualização da UTI.

### Modified Capabilities
- `solicitacao-leitos`: Ajustado para processar o formulário estruturado e permitir edição do Bloco antes da validação da UTI.
- `internacao-leitos`: Ajustado para expor permanentemente a ação de visualização da passagem de caso estruturada no card do leito.

## Impact

- **Banco de Dados (Modelos):** A coluna `passagem_caso` (JSON) na entidade `SolicitacaoLeito` armazenará o objeto estruturado do formulário.
- **API do Backend:**
  - O endpoint de finalização e atualização de cirurgia (`POST` e novo `PUT` de edição) receberá o payload JSON completo estruturado e fará as validações de campos obrigatórios.
  - O endpoint de listagem de leitos exporá o JSON estruturado para exibição do card.
- **Frontend (Vue):**
  - Modificação completa do modal de Passagem de Caso no painel de solicitações para renderizar as seções estruturadas e aplicar as validações de desabilitar botão.
  - Adição da funcionalidade de Edição de Passagem de Caso no Bloco Cirúrgico.
  - Adição do link/botão "Ver Passagem de Caso" no card do leito na UTI.
