## Why

Proteger os dados de saúde dos pacientes (nome, prontuário, diagnóstico, leito) retornados pelas rotas de listagem de leitos, exigindo autenticação obrigatória via token JWT para bloquear acessos não autorizados sem login.

## What Changes

- Adição da dependência `Depends(auth_handler.auth_wrapper)` no endpoint `GET /api/leitos` em `src/routers/leito.py`.
- Adição da dependência `Depends(auth_handler.auth_wrapper)` no endpoint `GET /api/leitos/disponiveis` em `src/routers/leito.py`.
- **BREAKING**: Requisições sem cabeçalho `Authorization: Bearer <token>` para `/api/leitos` passarão a retornar **401 Unauthorized** em vez de entregar a lista de pacientes.

## Capabilities

### New Capabilities
- `require-auth-leitos`: Exige autenticação obrigatoriamente para consulta de leitos e censo de pacientes da UTI.

### Modified Capabilities
*(Nenhuma especificação pré-existente alterada)*

## Impact

- **Backend (`src/routers/leito.py`)**: Inclusão do guard `auth_handler.auth_wrapper` nas funções `listar_leitos` e `listar_leitos_disponiveis_para_reserva`.
- **Segurança & LGPD**: Garante proteção dos dados pessoais de saúde de pacientes internados na UTI contra acesso anônimo/não autenticado.
