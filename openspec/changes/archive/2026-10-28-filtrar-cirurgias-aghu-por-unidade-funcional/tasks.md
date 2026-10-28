# Tasks: Filtrar Cirurgias do AGHU por Unidade Funcional Cirúrgica

## 1. Backend e Consulta SQL

- [x] 1.1 Em `src/providers/sql/solicitacao/obter_cirurgia_aghu.sql`, incluir a restrição `AND cir.unf_seq = ANY(:unf_seqs)` preservando a ordenação cronológica padrão.
- [x] 1.2 Em `src/providers/implementations/aghu_cirurgia_provider.py`, atualizar o método `obter_cirurgia_por_prontuario` para aceitar `unf_seqs: List[int]` e repassar o parâmetro à execução SQL.
- [x] 1.3 Em `src/controllers/solicitacao_leito_controller.py`, mapear o tipo de solicitação e perfil do usuário logado para as listas de unidades autorizadas (`BC`: `[28]`, `COB`: `[20]`, `HEM`: `[47, 233]`, default: `[28, 20, 47, 233]`).
- [x] 1.4 Em `src/routers/solicitacoes_leito.py`, atualizar o endpoint `GET /consultar-aghu/{prontuario}` para aceitar o parâmetro opcional `tipo: Optional[str] = Query(None)`.

## 2. Frontend

- [x] 2.1 Em `frontend/src/views/Solicitacoes.vue`, atualizar a função `buscarPacienteAghu` para repassar `formNova.value.tipo` como query parameter na consulta.
- [x] 2.2 Validar a compilação do frontend executando `npm run build`.

## 3. Validação e Documentação

- [x] 3.1 Testar a consulta do prontuário `22433189` no AGHU confirmando que retorna a cirurgia agendada de 06/11/2026 (Unidade 28) e ignora a endoscopia de 27/10/2026 (Unidade 155).
- [x] 3.2 Atualizar `CHANGELOG.md` e `docs/projeto_inicial/02-requisitos.md`.
