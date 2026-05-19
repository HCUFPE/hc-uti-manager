# faturamento-sus Specification

## Purpose
TBD - created by archiving change setup-openspec-docs. Update Purpose after archive.
## Requirements
### Requirement: Geração de AIH
O sistema MUST permitir a geração de Autorização de Internação Hospitalar (AIH) para faturamento no SUS.

#### Scenario: Geração de AIH com sucesso
- **WHEN** os dados do paciente e procedimento estão preenchidos
- **THEN** o sistema gera o arquivo magnético correspondente

### Requirement: Geração de BPA
O sistema MUST processar a produção ambulatorial (BPA).

#### Scenario: Processamento de BPA consolidado
- **WHEN** a consolidação mensal é requisitada
- **THEN** o sistema emite o lote BPA consolidado para faturamento

