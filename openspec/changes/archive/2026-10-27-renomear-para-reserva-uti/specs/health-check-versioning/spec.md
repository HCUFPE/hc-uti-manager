# Spec Delta

## MODIFIED Requirements

### Requirement: Fonte Única da Verdade para Versão (SSOT)
O sistema MUST centralizar o número de versão, nome oficial do sistema (`APP_NAME = "Reserva UTI"`), título do sistema, data da última atualização e metadados institucionais em um único módulo backend (`src/version.py`). O framework FastAPI (`src/main.py`), a rota `/api/health` e a documentação interativa Swagger `/docs` MUST carregar seus valores a partir deste módulo.

#### Scenario: Leitura de versão no Swagger e metadados da aplicação
- **WHEN** a aplicação FastAPI é inicializada
- **THEN** o título oficial "Reserva UTI", a versão e os metadados exibidos no Swagger SHALL ser importados de `src/version.py`
- **THEN** nenhuma versão estática ou nome legado divergente SHALL ser declarado no código-fonte do servidor
