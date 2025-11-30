#!/bin/bash

# Configuration
DATA_DIR="data"
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="data_backup_$TIMESTAMP.tar.gz"

# Create backups directory if it doesn't exist
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "Created backup directory: $BACKUP_DIR"
fi

# Create the backup
if [ -d "$DATA_DIR" ]; then
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" "$DATA_DIR"
    echo "✅ Backup created successfully: $BACKUP_DIR/$BACKUP_NAME"
else
    echo "❌ Error: Data directory '$DATA_DIR' not found!"
    exit 1
fi

# Optional: Keep only last 10 backups
cd "$BACKUP_DIR"
ls -t | tail -n +11 | xargs -I {} rm -- {}
cd ..
