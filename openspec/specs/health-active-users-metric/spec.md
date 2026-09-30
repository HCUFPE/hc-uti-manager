# health-active-users-metric Specification

## Purpose
TBD - created by archiving change v1-7-4-health-active-users. Update Purpose after archive.
## Requirements
### Requirement: Métrica de Usuários Ativos no Health Check
O endpoint `/api/health` MUST incluir no payload JSON de resposta a quantidade de usuários distintos com sessões ativas (`active_users`), calculados com base em tokens não expirados na tabela `refresh_tokens`.

#### Scenario: Consulta de status de saúde com métrica de usuários ativos
- **WHEN** uma requisição GET é enviada para `/api/health`
- **THEN** o backend retorna HTTP 200 com `"status": "healthy"`, versão atual `1.7.4` e o campo `"active_users"` contendo o número inteiro de usuários ativos distintos

#### Scenario: Tratamento de exceção no cálculo de usuários ativos
- **WHEN** ocorre uma falha na consulta à tabela de refresh tokens
- **THEN** o endpoint `/api/health` não quebra e retorna `"active_users": 0`, mantendo o status de saúde da aplicação

