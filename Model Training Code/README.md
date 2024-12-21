
# Model Training Code
**Derick Miller**  
**Dept. of Electrical and Computer Engineering**  
**Stevens Institute of Technology**  
**AAI646 Final Project**  

---

## Overview

This folder contains all necessary scripts, configurations, and utilities for training and evaluating object detection models on the JARVIS HPC. The training workflows for **YOLOv11** and **Faster R-CNN** are based on official documentation and external repositories, with custom improvements to enhance compatibility and streamline model performance.

- **YOLOv11**: Training scripts and configurations are adapted from the [Ultralytics YOLOv11 Documentation](https://docs.ultralytics.com), ensuring compatibility with SLURM-managed HPC environments and automating training pipelines.
- **Faster R-CNN**: Training scripts are based on the repository [FasterRCNN PyTorch Training Pipeline](https://github.com/sovit-123/fasterrcnn-pytorch-training-pipeline) by Sovit Ranjan Rath, with enhancements for efficient weight loading and better integration with the dataset.

---

## Preparing the Dataset

To train and evaluate the models, download the **SeaDroneSee** dataset from the [MACVi website](https://macvi.com). Once downloaded, follow these steps:

1. **Download and Organize the Dataset**:
   - Extract the dataset and place it into a directory. For example:
     ```
     /Data/SeaDroneSee/
         ├── Train/
         ├── Valid/
         ├── Test/
     ```

2. **Convert Labels to YOLO TXT Format**:
   - Use the provided `parse_json.py` script to convert the JSON annotations into YOLO-compatible TXT format.
   - Example command:
     ```bash
     python parse_json.py --input <path_to_json> --output <path_to_yolo_labels>
     ```

3. **For Faster R-CNN**:
   - Convert YOLO TXT labels into VOC XML format using the `convert_parallel.py` script.
   - Example command:
     ```bash
     python convert_parallel.py --yolo_path <path_to_yolo_labels> --voc_path <path_to_voc_annotations> --image_path <path_to_images>
     ```

---

## Model-Specific Instructions

### **1. YOLOv11**
- Navigate to the **YOLO11** folder for all relevant scripts and configurations.
- Follow the instructions in the **YOLO11 README** to:
  - Configure the `data.yaml` file for your dataset.
  - Schedule training, validation, and testing jobs using SLURM.
- Training is automated using scripts such as `schedule_yolo11.sh`, which can be submitted with:
  ```bash
  sbatch schedule_yolo11.sh
  ```

### **2. Faster R-CNN**
- Navigate to the **Faster R-CNN** folder for scripts and utilities.
- Follow the instructions in the **Faster R-CNN README** to:
  - Set up the dataset paths in `data.yaml`.
  - Automate the generation of training scripts using `edit_all_train.py`.
  - Schedule training, validation, and testing jobs with scripts like `Train_RCNN.sh`:
    ```bash
    sbatch Train_RCNN.sh
    ```

---

## Folder Structure

```
/Model_Training_Code
    ├── YOLO11/                    # YOLOv11-specific training scripts and configurations
    │   ├── schedule_yolo11.sh     # SLURM scheduler for YOLOv11 training
    │   ├── start_all.sh           # Automates submission of YOLOv11 jobs
    │   └── ...                    # Other YOLOv11 utilities
    ├── Faster_RCNN/               # Faster R-CNN-specific training scripts and configurations
    │   ├── Train_RCNN.sh          # SLURM scheduler for Faster R-CNN training
    │   ├── edit_all_train.py      # Automates Faster R-CNN script generation
    │   └── ...                    # Other Faster R-CNN utilities
    ├── parse_json.py              # Converts JSON annotations to YOLO TXT format
    ├── convert_parallel.py        # Converts YOLO TXT to VOC XML format
```

---

## Notes
- Ensure all paths and configurations are updated in the respective scripts and `data.yaml` files before running.
- Refer to the individual READMEs in the **YOLO11** and **Faster R-CNN** subfolders for detailed usage instructions.

For further assistance, refer to the [Ultralytics Documentation](https://docs.ultralytics.com) or [FasterRCNN PyTorch Training Pipeline Repository](https://github.com/sovit-123/fasterrcnn-pytorch-training-pipeline).
