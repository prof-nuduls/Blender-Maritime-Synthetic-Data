#!/bin/bash
yolo task=detect mode='predict' model=./runs/detect/train/weights/best.pt source='path_to/SeaDronesSee Object Detection v2/Uncompressed Version/Test/images' imgsz=1280 save_txt=True


