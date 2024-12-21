import os

# Base directory path where test_predict.py files should be created
base_dir = "./"
folders = ['pretrain',"only_real"]

# Loop through each folder and write the test_predict.py file
for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    file_path = os.path.join(folder_path, "yolo11_test.sh")
    
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Define the template as a regular multi-line string with custom placeholders
    template = """#!/bin/bash
yolo task=detect mode='predict' model=./runs/detect/train/weights/best.pt source='path_to/SeaDronesSee Object Detection v2/Uncompressed Version/Test/images' imgsz=1280 save_txt=True


"""
    # Replace placeholders with actual values
    script_content = template.replace("__base_dir__", base_dir).replace("__folder__", folder)
    
    # Write the test_predict.py file
    with open(file_path, 'w') as file:
        file.write(script_content)
    
    print(f"Created {file_path}")
