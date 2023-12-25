#!/bin/bash

# Source file path
source_file="/root/1224_web_server/database/account.db"

# Destination directory
backup_dir="/root/backup/"

# Create the backup directory if it doesn't exist
mkdir -p "$backup_dir"

# Get the current date and time
current_date_time=$(date +"%Y%m%d_%H%M%S")

# Destination file path with the current date and time
destination_file="$backup_dir/test-$current_date_time.db"

# Check if the last backup exists
last_backup=$(ls -t "$backup_dir" | head -n1)
last_backup_file="$backup_dir/$last_backup"

# Compare the content of the source file with the last backup
if [ -f "$last_backup_file" ] && cmp -s "$source_file" "$last_backup_file"; then
    # If the content is the same, update the timestamp of the last backup
    mv "$last_backup_file" "$backup_dir/test-$current_date_time.db"
    echo "File content unchanged. Updated timestamp of the last backup."
else
    # If the content is different, create a new backup
    cp "$source_file" "$destination_file"
    echo "File content changed. Created a new backup: $destination_file"
fi
