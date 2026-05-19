## 1. Backend

- [x] 1.1 Atualizar a rota `DELETE /api/solicitacoes/{sol_id}` no arquivo `src/routers/solicitacoes_leito.py` para aceitar um parâmetro opcional ou obrigatório de `motivo` (via query string).
- [x] 1.2 Atualizar a chamada ao `historico.registrar` dentro da rota de exclusão para incluir o `motivo` na string de detalhes (ex: `Motivo: A`).

## 2. Frontend

- [x] 2.1 Criar uma constante com a lista de motivos pré-definidos (Motivo A, Motivo B, Motivo C).
- [x] 2.2 Modificar o componente que chama o cancelamento de leito para exibir um Modal ou `prompt/select` perguntando o motivo.
- [x] 2.3 Atualizar a chamada à API (`axios.delete` ou equivalente) para enviar o motivo escolhido como parâmetro.
