#!/bin/bash
#SBATCH --job-name=pre-train-FR-val     # Job name reflecting folder/model
#SBATCH --output=output_%j.txt                # Standard output log
#SBATCH --error=error_%j.txt                  # Standard error log
#SBATCH --time=24:00:00                       # Time limit (10 hours)
#SBATCH --partition=compute                 # GPU partition
#SBATCH --ntasks=1                            # One task
#SBATCH --cpus-per-task=8                     # Request 8 CPU cores

python eval.py --model fasterrcnn_resnet50_fpn_v2 --weights /outputs/training/pre-train_Faster_RCNN_v2_p30/best_model.pth --data "/Data/Faster-RCNN/pre-train/data_configs/data.yaml" --imgsz 1280 --batch 4 --verbose