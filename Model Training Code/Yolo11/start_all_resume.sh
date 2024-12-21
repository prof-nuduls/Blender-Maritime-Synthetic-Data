#!/bin/bash

# Array of directories to process
#folders=("0%" "25%" "50%" "75%" "100%")
folders=("+25k" "+50k" "+90k")
# Base path where the folders are located
base_path="/mmfs1/home/dmiller10/EE800 Research/Code/Yolo11/models/300_epochs_x"

# Loop through each folder and submit the job
for folder in "${folders[@]}"; do
    folder_path="$base_path/$folder"

    # Check if schedule_yolo.sh exists in the folder
    if [ -f "$folder_path/schedule_yolo_resume.sh" ]; then
        echo "Submitting job in $folder_path"
        
        # Change into the directory and submit the job
        (cd "$folder_path" && sbatch schedule_yolo_resume.sh)
    else
        echo "schedule_yolo.sh not found in $folder_path. Skipping..."
    fi
done
