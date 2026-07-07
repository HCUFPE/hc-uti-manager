# usuarios-perfis-migracao Specification

## Purpose
TBD - created by archiving change clean-db-backfill-ad-profiles. Update Purpose after archive.
## Requirements
### Requirement: Preservação de Perfis no Reset do Banco
A rotina de limpeza de dados transacionais na VM MUST preservar os perfis de acesso cadastrados localmente no banco, limpando apenas dados operacionais.

#### Scenario: Execução da limpeza preservando perfis
- **WHEN** o desenvolvedor executa o script de limpeza de banco de dados na VM
- **THEN** os dados das tabelas `solicitacoes_leito`, `solicitacoes_alta`, `historico_acoes`, `alertas`, `refresh_tokens` e `leito_estados` SHALL ser apagados
- **THEN** as configurações de perfis na tabela `usuarios_perfis` SHALL ser mantidas inalteradas

### Requirement: Carga de Dados do AD (Backfill)
O sistema MUST prover um script utilitário capaz de sincronizar em lote as informações de Nome Completo, Lotação e E-mail a partir do AD para os perfis que já estão salvos no banco SQLite local da VM.

#### Scenario: Execução da carga de dados retroativa (Backfill)
- **WHEN** o desenvolvedor executa o script de backfill de perfis
- **THEN** o script SHALL conectar-se à VM e consultar todos os registros da tabela `usuarios_perfis`
- **THEN** para cada usuário listado, o script SHALL buscar seus atributos de Nome, Setor e E-mail no Active Directory
- **THEN** o script SHALL gravar os atributos consultados de volta nas colunas `nome_completo`, `lotacao` e `email` da tabela correspondente na VM

