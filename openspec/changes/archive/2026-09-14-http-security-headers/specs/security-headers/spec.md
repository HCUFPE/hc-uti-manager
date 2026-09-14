## ADDED Requirements

### Requirement: Security Headers Middleware Implementation
O backend em FastAPI MUST injetar os cabeçalhos de segurança HTTP em todas as respostas de requisições HTTP recebidas pela aplicação.

#### Scenario: Verify response headers on API request
- **WHEN** uma requisição HTTP for realizada para qualquer endpoint do backend (ex: `/api/health` ou `/api/v1/beds`)
- **THEN** a resposta HTTP retornado pelo servidor MUST conter os seguintes cabeçalhos exatamente definidos:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
  - `Pragma: no-cache`
