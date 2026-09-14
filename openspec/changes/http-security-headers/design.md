## Context

O HC-UTI Manager utiliza FastAPI como framework backend. Para estar totalmente alinhado aos padrões de segurança do Framework SETISD e às boas práticas de segurança em saúde hospitalar, é necessário que todas as rotas REST retornem automaticamente cabeçalhos HTTP que impeçam o armazenamento de dados sensíveis em cache e protejam a aplicação contra ataques como Clickjacking, MIME-sniffing e XSS.

## Goals / Non-Goals

**Goals:**
- Implementar um middleware global `@app.middleware("http")` no FastAPI (`src/main.py`).
- Garantir que cada resposta da API contenha os 5 cabeçalhos de segurança definidos no padrão do Framework:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
  - `Pragma: no-cache`

**Non-Goals:**
- Alterar configurações de CORS (já configuradas e funcionais).
- Alterar cabeçalhos no nível do Nginx/proxy reverso da VM de homologação/produção (a tratativa será feita diretamente pela aplicação FastAPI).

## Decisions

- **Middleware no nível da aplicação FastAPI (`src/main.py`)**:
  - *Decisão*: Utilizar `@app.middleware("http")` do FastAPI.
  - *Razão*: É simples, centralizado e garante que todas as rotas (incluindo rotas futuras) herdem automaticamente os cabeçalhos de segurança sem necessidade de decoradores individuais ou alteração nas configurações do servidor web.

## Risks / Trade-offs

- **[Risco] Interrupção de cache para recursos estáticos da API**: Como a API serve dados dinâmicos JSON de UTI, o cabeçalho `no-store` é extremamente benéfico para a segurança dos pacientes e não afeta o desempenho da interface Vue.js (já que o frontend é servido separadamente pelo Nginx/Vite).
