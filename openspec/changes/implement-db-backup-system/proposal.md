## Why

Para garantir a integridade dos dados da aplicação HC-UTI Manager, é fundamental ter uma política de backups automáticos periódicos (diários) e backups preventivos antes de qualquer deploy/rebuild do sistema.

## What Changes

- Script de Deploy: Adicionar o passo de backup preventivo em `scratch/git_pull_and_rebuild.py` antes de reiniciar o serviço.
- Script do Host: Criar um shell script em `scratch/backup_db.sh` para ser configurado no cron diário da VM.
- Documentação: Documentar no README como instalar o cron diário na VM.

## Capabilities

### New Capabilities
- `implement-db-backup-system`: Sistema de backup automático e preventivo do banco SQLite.

## Impact

- `scratch/git_pull_and_rebuild.py`
- `scratch/backup_db.sh`
- `README.md`
