#!/bin/bash

# Array of directories to process
folders=("pretrain","only_real")
# Base path where the folders are located
base_path="./"

# Loop through each folder and submit the job
for folder in "${folders[@]}"; do
    folder_path="$base_path/$folder"

    # Check if schedule_yolo.sh exists in the folder
    if [ -f "$folder_path/schedule_yolo_val.sh" ]; then
        echo "Submitting job in $folder_path"
        
        # Change into the directory and submit the job
        (cd "$folder_path" && sbatch schedule_yolo_val.sh)
    else
        echo "schedule_yolo.sh not found in $folder_path. Skipping..."
    fi
done
