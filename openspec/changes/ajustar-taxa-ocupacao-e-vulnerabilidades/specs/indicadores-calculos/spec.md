## ADDED Requirements

### Requirement: Cálculo da Taxa de Ocupação com Leitos Mockados
O painel de indicadores MUST exibir a taxa de ocupação instantânea baseada nos leitos obtidos do censo. Caso a injeção de leitos de teste esteja ativa (`MOCK_BEDS=true` em desenvolvimento), a taxa de ocupação MUST ser calculada com base nos leitos mockados injetados, reconhecendo o status de ocupação de forma insensível a maiúsculas/minúsculas.

#### Scenario: Cálculo da taxa de ocupação em desenvolvimento com MOCK_BEDS ativa
- **WHEN** o usuário acessa o painel de indicadores gerais com `MOCK_BEDS=true`
- **THEN** o sistema calcula a taxa de ocupação utilizando a lista de leitos mockados e retorna o percentual correto na resposta
