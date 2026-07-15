## ADDED Requirements

### Requirement: Cálculo do Tempo Médio de Higienização de Leitos da UTI
O sistema MUST calcular o tempo médio (em minutos) em que os leitos de UTI permanecem no status de higienização ("LIMPEZA") com base no histórico de transições de status do AGHU (`agh.ain_extrato_leitos`) pertencentes a leitos da UTI (`unf_seq = 115`).

#### Scenario: Cálculo do tempo de higienização com sucesso
- **WHEN** o sistema recupera e analisa o histórico de extrato de leitos de UTI no período filtrado
- **THEN** o sistema calcula a diferença de tempo entre a entrada em "LIMPEZA" e a transição para o próximo status de cada leito, retornando a média geral em minutos
