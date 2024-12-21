#!/bin/bash
#!/bin/bash

yolo train resume model=./runs/detect/train/weights/last.pt 
yolo task=detect mode='val' model=./runs/detect/train/weights/best.pt data='base_path/data.yaml'


