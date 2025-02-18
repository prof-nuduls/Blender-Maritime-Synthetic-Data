#!/bin/bash
#SBATCH --job-name=fine-tuned-FR-300epochs      # Job name reflecting folder/model
#SBATCH --output=output_%j.txt                # Standard output log
#SBATCH --error=error_%j.txt                  # Standard error log
#SBATCH --time=24:00:00                       # Time limit (10 hours)
#SBATCH --partition=compute                 # GPU partition
#SBATCH --ntasks=1                            # One task
#SBATCH --cpus-per-task=8                     # Request 8 CPU cores

python inference.py --input /mmfs1/home/dmiller10/EE800\ Research/Data/SeaDronesSee\ Object\ Detection\ v2/Uncompressed\ Version/Test/images --model fasterrcnn_resnet50_fpn_v2 --weights ./outputs/training/finetune_Faster_RCNN_v2_p30/best_model.pth --imgsz 1280 --output ./test_results2 --log-json