## 1. Backend: Injetar Nome e Hora da Cirurgia

- [x] 1.1 Atualizar `listar_leitos` no arquivo `src/controllers/leitos_controller.py` para injetar `nome_proximo` e `hora_cirurgia_proximo` no leito a partir da solicitação associada
- [x] 1.2 Atualizar leitos mockados na listagem de desenvolvimento em `src/controllers/leitos_controller.py` com `nome_proximo` e `hora_cirurgia_proximo` fictícios para validar visualmente

## 2. Frontend: Mapear e Exibir Dados no Card do Leito

- [x] 2.1 Atualizar a definição do tipo `Patient` em `frontend/src/views/Home.vue` e `frontend/src/components/BedCard.vue` para incluir `nome?: string` e `horaCirurgia?: string`
- [x] 2.2 Atualizar o mapeamento do `proximoPaciente` no arquivo `frontend/src/views/Home.vue` para mapear `nome` e `horaCirurgia` vindos da API
- [x] 2.3 Modificar o template de `frontend/src/components/BedCard.vue` para exibir o nome do próximo paciente abaixo do prontuário e usar a hora da cirurgia concatenada no formato `DD/MM/AAAA - HH:MM`
