## Why

O banco de dados de produção na VM precisa de limpezas periódicas de dados transacionais para testes ou reset de ambiente. Os perfis de acesso customizados (`usuarios_perfis`) devem ser preservados para evitar o recadastro manual dos usuários. Adicionalmente, com a criação das novas colunas cadastrais (`nome_completo`, `lotacao`, `email`), os registros de perfis existentes no banco local da VM estão sem esses dados. É necessária uma rotina que consulte o AD e preencha retroativamente (backfill) esses dados cadastrais para todos os usuários com perfis ativos.

## What Changes

- **Limpeza Preservativa do Banco**: Confirmar/garantir que o script de limpeza `scratch/clean_vm_db.py` exclua apenas dados de transações (solicitações de leito, solicitações de alta, histórico de ações, alertas, refresh tokens e estados dos leitos), mantendo intocada a tabela `usuarios_perfis`.
- **Carga de Dados Retroativa (Backfill)**: Criar um script utilitário `scratch/backfill_ad_details.py` que:
  - Se conecte à VM via SSH.
  - Consulte o banco SQLite local `/var/app/hc-uti-manager/data/app.db` para listar todos os usuários cadastrados em `usuarios_perfis`.
  - Para cada usuário, faça uma consulta ao Active Directory (AD) configurado na VM (usando a conta de serviço) para recuperar seu Nome Completo, Lotação e E-mail.
  - Atualize essas três colunas na tabela local `usuarios_perfis` da VM.

## Capabilities

### New Capabilities
- `usuarios-perfis-migracao`: Ferramentas utilitárias para sincronização em lote e backfill de informações cadastrais do AD para perfis de acesso existentes no banco de dados local.

### Modified Capabilities
<!-- None -->

## Impact

- **Utilitários de Desenvolvimento**:
  - `scratch/clean_vm_db.py`: Certificar de que não afeta a tabela de perfis de acesso.
  - `scratch/backfill_ad_details.py`: Novo script utilitário para execução em lote via console do desenvolvedor.
