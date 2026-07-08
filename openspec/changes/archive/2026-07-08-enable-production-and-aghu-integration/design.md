## Context

A aplicação está rodando em homologação/produção com `MOCK_BEDS=true` no arquivo `.env` da VM e com dados fictícios populados na base SQLite (`app.db`), incluindo usuários administrativos e operacionais de teste (`admin`, `bloco`, `nir`, `uti`). Para iniciar a operação real, precisamos remover essas informações de simulação e ativar a integração de dados reais com o banco de dados do AGHU.

## Goals / Non-Goals

**Goals:**
- Desativar o modo mockado (`MOCK_BEDS=false`) no ambiente de produção/homologação.
- Excluir permanentemente todos os registros de reservas, solicitações de alta e histórico de simulações do banco local.
- Remover os usuários de teste padrão (`admin`, `bloco`, `nir`, `uti`), mantendo os usuários cadastrados e o login exclusivo pelo Active Directory.
- Habilitar todas as consultas reais ao banco de dados do AGHU.

**Non-Goals:**
- Alterar a estrutura das tabelas ou realizar migrations de schema.
- Excluir usuários reais que já foram inseridos no banco.

## Decisions

- **Script de Limpeza Temporário (`production_cleanup.py`):** Criaremos um script em Python rodando dentro do container para limpar as tabelas da base SQLite de forma segura usando SQLAlchemy.
- **Substituição de Configurações via Sed:** Utilizaremos um comando `sed` no host da VM para alterar o arquivo `/var/app/hc-uti-manager/.env`, mudando `MOCK_BEDS=true` para `MOCK_BEDS=false`.

## Risks / Trade-offs

- **Perda de Dados Históricos:** A limpeza da base de dados local apagará o histórico atual.
  - *Mitigação:* Como se trata de dados simulados/mockados de teste, a perda é planejada e desejada.
