#!/bin/bash
#SBATCH --job-name=pretrain-Yolo11x      # Job name
#SBATCH --output=output_%j.txt          # Standard output log
#SBATCH --error=error_%j.txt            # Standard error log
#SBATCH --time=24:00:00                 # Time limit (10 hours)
#SBATCH --partition=gpu-l40s           # GPU partition
#SBATCH --ntasks=1                      # One task
#SBATCH --cpus-per-task=4               # Request 4 CPU cores
#SBATCH --mem=48G                      # Memory request (150 GB)
#SBATCH --gres=gpu:1                    # Request 4 GPUs


pip install --user ultralytics supervision
# Run the script using all 4 GPUs (0,1,2,3)
srun ./yolo11.sh
