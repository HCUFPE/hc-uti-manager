## Goals / Non-Goals

**Goals:**
- Proteger contra falhas de migrações ou deploy de bugs.
- Garantir histórico de backups diários rotativos para recuperação em desastres.

## Decisions

### 1. Deploy Backup (Preventivo)
Em `scratch/git_pull_and_rebuild.py`, adicionaremos o seguinte comando antes da reinicialização do compose:
`podman exec hc-uti-backend sqlite3 /app/data/app.db ".backup '/app/data/backup_pre_deploy.db'"`
Como o contêiner `hc-uti-backend` estará ativo na hora em que o script roda (antes de fazermos `systemctl restart`), podemos utilizar o próprio binário `sqlite3` interno do container para fazer o backup de forma 100% segura.

### 2. Cron Backup (Histórico Rotativo de 7 dias)
Criaremos um script em `scratch/backup_db.sh` para ser executado no host da VM. Este script:
1. Cria a pasta `/var/app/hc-uti-manager/data/backups/` se não existir.
2. Faz o backup seguro via comando `sqlite3`.
3. Compacta o arquivo com gzip (opcional, mas bom padrão, embora o banco seja pequeno).
4. Remove os backups com mais de 7 dias de idade utilizando `find ... -mtime +7 -delete` para evitar vazamento de espaço em disco.
