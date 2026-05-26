## 1. Frontend Implementation

- [x] 1.1 Em `frontend/src/views/Home.vue`, criar a variável reativa para armazenar as necessidades selecionadas e as opções fixas de necessidades.
- [x] 1.2 Implementar a lógica de exclusão mútua (`onNecessidadeChange`) na seleção dos checkboxes no frontend.
- [x] 1.3 Substituir o campo `<textarea>` no modal de solicitar alta em `frontend/src/views/Home.vue` pelo grupo de checkboxes.
- [x] 1.4 No método `confirmarSolicitacaoAlta`, serializar o array de necessidades selecionadas em uma única string separada por vírgula (ou "Nenhum" se vazio) antes do envio para a API.

## 2. Verification

- [x] 2.1 Testar manualmente a solicitação de alta marcando múltiplos itens e verificar se a string é salva de forma concatenada no SQLite e exibida corretamente nas telas.
- [x] 2.2 Testar manualmente o cenário com a opção "Nenhum" selecionada (ou nenhuma opção marcada) e validar a persistência.
