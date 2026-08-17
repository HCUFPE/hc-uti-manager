#!/bin/bash
# Script de backup diário rotativo do banco de dados SQLite do HC-UTI Manager

DATA_DIR="/var/app/hc-uti-manager/data"
BACKUP_DIR="$DATA_DIR/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.db"

# Garante que a pasta de backups exista
mkdir -p "$BACKUP_DIR"

echo "Iniciando backup do SQLite..."

# Faz o backup usando o container se ele estiver ativo (utilizando Python nativo para evitar dependência do binário sqlite3)
if podman ps | grep -q "hc-uti-backend"; then
    podman exec hc-uti-backend python -c "import sqlite3; conn = sqlite3.connect('/app/data/app.db'); dest = sqlite3.connect('/app/data/backups/backup_$TIMESTAMP.db'); conn.backup(dest); conn.close(); dest.close()"
else
    # Fallback se o container estiver offline e tiver sqlite3 no host
    if command -v sqlite3 &> /dev/null; then
        sqlite3 "$DATA_DIR/app.db" ".backup '$BACKUP_FILE'"
    else
        # Simples cp se não tiver sqlite3 no host
        cp "$DATA_DIR/app.db" "$BACKUP_FILE"
    fi
fi

# Compacta o arquivo para economizar espaço
if [ -f "$BACKUP_DIR/backup_$TIMESTAMP.db" ]; then
    gzip "$BACKUP_DIR/backup_$TIMESTAMP.db"
    echo "Backup gerado com sucesso: backup_$TIMESTAMP.db.gz"
else
    echo "Falha ao gerar o arquivo de backup."
    exit 1
fi

# Remove backups com mais de 7 dias
find "$BACKUP_DIR" -name "backup_*.db.gz" -mtime +7 -delete
echo "Rotação de backups antiga concluída."
