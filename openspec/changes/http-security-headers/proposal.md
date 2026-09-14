## Why

Alinhamento do backend FastAPI do HC-UTI Manager com o padrão oficial do Framework SETISD / HC-UFPE, garantindo que respostas HTTP incluam cabeçalhos de segurança cruciais (Security Headers) para proteger dados sensíveis de pacientes e leitos contra cache indevido em terminais públicos e ataques comuns da web.

## What Changes

- Adição do middleware HTTP de Security Headers (`add_security_headers`) no ponto de entrada do backend (`src/main.py`).
- Injeção automática dos seguintes cabeçalhos de segurança HTTP em todas as respostas da API:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
  - `Pragma: no-cache`

## Capabilities

### New Capabilities
- `security-headers`: Adiciona middleware global no FastAPI para envio obrigatório de cabeçalhos de segurança HTTP nas respostas REST.

### Modified Capabilities
*(Nenhuma especificação pré-existente alterada)*

## Impact

- **Backend (`src/main.py`)**: Atualização do arquivo principal para importar `Request` do `fastapi` e adicionar a função `@app.middleware("http")`.
- **Segurança & Privacidade**: Bloqueia cache de dados hospitalares em navegadores de setores/postos de enfermagem após logout e previne Clickjacking/MIME-sniffing.
