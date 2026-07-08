## Why

O sistema atualmente opera em modo de demonstração com dados mockados (como pacientes simulados na UTI) e usuários fictícios de teste (`admin`, `bloco`, `nir`, `uti`). Para iniciar a operação real em produção, é necessário limpar esses dados de teste da base SQLite do servidor e ativar de forma definitiva as conexões reais com o banco de dados do AGHU.

## What Changes

- **Limpeza de Banco de Dados:** Exclusão de todas as tabelas de dados de simulação da base SQLite na VM de homologação/produção.
- **Remoção de Usuários de Teste:** Exclusão dos usuários mockados (`admin`, `bloco`, `nir`, `uti`) do banco de dados SQLite, mantendo apenas os usuários reais cadastrados e integrados via LDAP.
- **Desativação de Mockups:** Desativação completa dos geradores de dados mockados e dos pacientes falsos no backend Python.
- **Integração Plena com o AGHU:** Configuração e ativação de todas as rotas e queries diretas ao banco de dados do AGHU PostgreSQL/Oracle para exibição em tempo real do censo e das cirurgias.

## Capabilities

### New Capabilities
Nenhuma.

### Modified Capabilities
- `internacao-leitos`: A listagem de leitos e o gerenciamento de reservas passarão a utilizar dados dinâmicos reais obtidos diretamente da API integradora do AGHU, em vez de gerar dados simulados em memória ou banco local.

## Impact

- **Backend:** Alteração das flags de inicialização no `src/main.py` ou de carregamento de mocks nos controllers de leito e solicitações.
- **Banco de Dados (SQLite):** Execução de script de limpeza ou migrations para remoção de registros de teste e expiração de sessões anteriores.
- **Infraestrutura:** Reinicialização dos containers com as novas configurações de produção.
