## Requirements

### Requirement: Preventative deploy backup
The deployment pipeline script SHALL generate a database backup before updating the system.

#### Scenario: Running deploy pipeline
- **WHEN** the `git_pull_and_rebuild.py` script starts and executes on the VM
- **THEN** it SHALL perform a backup of the current database to `backup_pre_deploy.db` inside `/var/app/hc-uti-manager/data/` prior to container recreation.

### Requirement: Daily scheduled backup script
The codebase SHALL contain a shell script designed to be run on the host VM cron system to perform periodic database backups.

#### Scenario: Running the backup shell script
- **WHEN** `backup_db.sh` is executed on the VM host
- **THEN** it SHALL create a timestamped backup of `/var/app/hc-uti-manager/data/app.db` under a `backups/` directory, keeping only the 7 most recent backups to save disk space.
