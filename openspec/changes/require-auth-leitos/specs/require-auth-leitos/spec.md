## ADDED Requirements

### Requirement: Authentication Required for Bed Listing
As rotas de consulta de leitos do backend MUST exigir um token JWT de autenticação válido para entregar as informações dos pacientes e leitos.

#### Scenario: Anonymous user attempts to list beds
- **WHEN** uma requisição HTTP GET for enviada para `/api/leitos` ou `/api/leitos/disponiveis` sem o cabeçalho `Authorization: Bearer <token>`
- **THEN** o backend MUST responder com status HTTP 401 Unauthorized e bloquear o acesso aos dados dos pacientes.

#### Scenario: Authenticated user requests bed list
- **WHEN** uma requisição HTTP GET for enviada para `/api/leitos` contendo um token JWT de autenticação válido no cabeçalho `Authorization`
- **THEN** o backend MUST responder com status HTTP 200 OK e entregar a lista de leitos.
