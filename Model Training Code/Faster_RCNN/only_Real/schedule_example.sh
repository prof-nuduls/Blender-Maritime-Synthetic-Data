#!/bin/bash
#SBATCH --job-name=Test-FasterRCNN-0%      # Job name
#SBATCH --output=output_%j.txt          # Standard output log
#SBATCH --error=error_%j.txt            # Standard error log
#SBATCH --time=24:00:00                 # Time limit (10 hours)
#SBATCH --partition=gpu-l40s            # GPU partition
#SBATCH --ntasks=1                      # One task
#SBATCH --cpus-per-task=4               # Request 4 CPU cores
#SBATCH --mem=150G                      # Memory request (150 GB)
#SBATCH --gres=gpu:4                   # Request 4 GPUs


python -m torch.distributed.launch --nproc_per_node=4 --use_env train.py \
    --data "/mmfs1/home/dmiller10/EE800 Research/Data/Faster-RCNN/0%/data_configs/data.yaml" \
    --epochs 30 \
    --model fasterrcnn_resnet50_fpn \
    --name Faster_RCNN \
    --batch 16 \
    --disable-wandb \
    --imgsz 640

	