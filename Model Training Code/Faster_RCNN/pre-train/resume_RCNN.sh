#!/bin/bash
#SBATCH --job-name=pre-train-FR-300epochs      # Job name reflecting folder/model
#SBATCH --output=output_%j.txt                # Standard output log
#SBATCH --error=error_%j.txt                  # Standard error log
#SBATCH --time=24:00:00                       # Time limit (10 hours)
#SBATCH --partition=gpu-l40s                  # GPU partition
#SBATCH --ntasks=1                            # One task
#SBATCH --cpus-per-task=8                     # Request 8 CPU cores
#SBATCH --mem-per-gpu=48G                     # Memory per GPU
#SBATCH --gres=gpu:1                        # Request 4 GPUs

export MASTER_ADDR=localhost
export MASTER_PORT=29501
export CUDA_VISIBLE_DEVICES=0

python -m torch.distributed.launch --nproc_per_node=1 --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT --use-env train.py      --data "/Faster-RCNN/pre-train/data_configs/data.yaml"     --epochs 300     --resume-training     --model fasterrcnn_resnet50_fpn_v2     --name pre-train_Faster_RCNN_v2_p30     --batch 8     --imgsz 1920     --patience 50
