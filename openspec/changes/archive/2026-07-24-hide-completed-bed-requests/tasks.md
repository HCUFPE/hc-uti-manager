## 1. Backend Integration

- [x] 1.1 Atualizar `src/controllers/solicitacao_leito_controller.py` (método `listar_solicitacoes`) para incluir o campo `"atualizado_em"` no dicionário de cada solicitação, formatado como string no padrão Brasília de data/hora (`"%Y-%m-%d %H:%M"` ou similar).

## 2. Frontend Layout & Logic

- [x] 2.1 Adicionar uma propriedade reativa no script de `frontend/src/views/Solicitacoes.vue` para controlar a expansão das solicitações concluídas: `const concluidaExpandida = ref(false)`.
- [x] 2.2 Atualizar o template de `frontend/src/views/Solicitacoes.vue` na seção de solicitações concluídas para torná-la colapsável, adicionando um botão de toggle com ícones apropriados e animando/mostrando a lista de cards apenas quando expandido.
- [x] 2.3 Exibir a data e hora de conclusão (a partir de `sol.atualizado_em` vindo do backend) em tamanho pequeno dentro de cada card na seção de solicitações concluídas.
