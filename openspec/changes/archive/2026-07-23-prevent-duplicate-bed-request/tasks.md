## 1. Backend Dependencies and Injection

- [x] 1.1 Atualizar o construtor do `SolicitacaoLeitoController` em `src/controllers/solicitacao_leito_controller.py` para aceitar um `census_provider: LeitoProviderInterface | None = None` opcional.
- [x] 1.2 Atualizar a função de injeção `get_solicitacao_leito_controller` em `src/dependencies.py` para passar o `census_provider` (obtido via dependência `_get_leito_aghu_provider`) ao instanciar o `SolicitacaoLeitoController`.

## 2. Validação no Backend

- [x] 2.1 Adicionar validação de censo em `criar_solicitacao` no `SolicitacaoLeitoController`: se `census_provider` estiver ativo, buscar leitos e validar se o `prontuario` informado já consta como `prontuario_atual`. Lançar `HTTPException(status_code=400, detail="O paciente deste prontuário já ocupa o Leito X da UTI! A solicitação não poderá ser criada.")`.
- [x] 2.2 Adicionar a mesma validação de censo no método `editar_solicitacao` do `SolicitacaoLeitoController` no bloco onde ocorre a troca de prontuário, garantindo que o novo prontuário informado também seja validado contra o censo físico de leitos ativos da UTI.
