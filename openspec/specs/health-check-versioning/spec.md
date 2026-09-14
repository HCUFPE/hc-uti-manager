# health-check-versioning Specification

## Purpose
Estabelecer um padrão unificado de versionamento (Single Source of Truth) e um endpoint padronizado de monitoramento e telemetria (`/api/health`) para consumo de clientes, sondas de infraestrutura e reatividade no frontend.

## Requirements

### Requirement: Endpoint de Monitoramento e Saúde (/api/health)
O sistema MUST disponibilizar um endpoint REST HTTP `GET /api/health` público que verifique a conectividade ativa dos bancos de dados configurados (`app_db` e `aghu_postgres`), e forneça metadados de versão, identidade organizacional e timestamp UTC da aplicação.

#### Scenario: Consulta de saúde com todos os bancos saudáveis
- **WHEN** uma sonda de monitoramento ou o cliente frontend realiza uma requisição `GET /api/health`
- **THEN** o sistema SHALL executar uma checagem ativa (`SELECT 1`) nas conexões de banco de dados
- **THEN** o sistema SHALL responder com status code HTTP 200 OK e JSON contendo `status: "healthy"`, versão oficial, metadados institucionais e o dicionário de status dos bancos

#### Scenario: Falha no banco de dados local essencial
- **WHEN** o banco de dados principal `app_db` estiver inacessível ou falhar ao executar a checagem
- **THEN** o sistema SHALL registrar o erro no dicionário de bancos
- **THEN** o sistema SHALL responder com status code HTTP 503 SERVICE UNAVAILABLE e `status: "unhealthy"`

### Requirement: Fonte Única da Verdade para Versão (SSOT)
O sistema MUST centralizar o número de versão, data da última atualização e metadados institucionais em um único módulo backend (`src/version.py`). O framework FastAPI (`src/main.py`), a rota `/api/health` e a documentação interativa Swagger `/docs` MUST carregar seus valores a partir deste módulo.

#### Scenario: Leitura de versão no Swagger e metadados da aplicação
- **WHEN** a aplicação FastAPI é inicializada
- **THEN** o título e a versão exibidos nos metadados OpenAPI/Swagger SHALL ser importados de `src/version.py`
- **THEN** nenhuma versão estática divergente SHALL ser declarada no código-fonte do servidor

### Requirement: Consumo Reativo de Versão no Frontend
O frontend MUST possuir uma store reativa que realiza uma requisição para `/api/health` durante a inicialização da aplicação, atualizando os valores reativos de versão e data da última atualização exibidos nos componentes de interface (ex.: menu lateral e tela de login).

#### Scenario: Atualização automática da versão no menu e login
- **WHEN** a aplicação frontend é carregada no navegador do usuário
- **THEN** a store de versão SHALL disparar a busca em `/api/health`
- **THEN** os componentes que exibem a versão e data de atualização SHALL atualizar dinamicamente para os valores retornados pelo backend
- **THEN** em caso de indisponibilidade momentânea da API, o frontend SHALL manter valores de fallback seguros sem quebrar a interface
