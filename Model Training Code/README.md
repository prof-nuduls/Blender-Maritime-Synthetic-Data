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

### **1. Data Download and Organization**

#### **SeaDronesSee Object Detection v2 Dataset**
- Download the dataset from [MACVi](https://macvi.com).
- The dataset contains `Train`, `Valid`, and `Test` splits, stored in `Compressed` and `Uncompressed` formats.
- Annotation files are provided separately in JSON format.
- Example directory structure:
  ```
  /Data/SeaDronesSee Object Detection v2/
      ├── Compressed/
      │   ├── Train/
      │   ├── Valid/
      │   ├── Test/
      ├── Uncompressed/
      │   ├── Train/
      │   ├── Valid/
      │   ├── Test/
      ├── Annotations/
          ├── instances_train.json
          ├── instances_valid.json
          ├── instances_test.json
  ```

### **2. File Conversion**

#### **Convert JSON to YOLO TXT**
- Use `parse_json.py` to convert JSON annotations to YOLO TXT format.
- Command:
  ```bash
  python parse_json.py --input /path/to/json --output /path/to/yolo_labels
  ```
- Example output directory:
  ```
  /Data/SeaDronesSee Object Detection v2/
      ├── Train/
      │   ├── images/
      │   ├── labels/
      ├── Valid/
      │   ├── images/
      │   ├── labels/
      ├── Test/
          ├── images/
          ├── labels/
  ```

#### **Convert YOLO TXT to VOC XML**
- Use `convert_parallel.py` to generate VOC XML annotations for Faster R-CNN.
- Command:
  ```bash
  python convert_parallel.py --yolo_path /path/to/yolo_labels --voc_path /path/to/voc_annotations --image_path /path/to/images
  ```
- Example output directory:
  ```
  /Data/Faster-RCNN/
      ├── Train/
      │   ├── images/
      │   ├── annotations/
      ├── Valid/
      │   ├── images/
      │   ├── annotations/
  ```

---

## Model Training

### **Mass Editing Scripts**

#### **Overview**
Mass editing scripts allow for efficient and uniform modifications across multiple training, validation, and test files for different dataset splits. This ensures consistency and saves time when adjusting parameters or configurations.

#### **Examples of Mass Editing Scripts**

**YOLO11 mass file edits**
- `edit_yolo11_script.py`: Modify all training scripts.
- `edit_yolo11_script_schedule.py`: Modify all training scheduler script.
- `edit_yolo11_script_test.py`: Modify testing scripts.
- `edit_yolo11_script_val.py`: Modify validation scripts.  


**Faster R-CNN mass file edits**
- `edit_all_train.py`: Modify all training scripts.
- `edit_all_val.py`: Modify validation scripts.
- `edit_all_test.py`: Modify testing scripts.
- `edit_all_resume.py`: Modify resume training scripts.



#### **Usage**
To execute a mass editing script, simply edit the template inside the script and run the file.

```bash
python edit_all_train.py 
```

This will apply the specified changes across all relevant files, for the base dir, and folders specified.



### **YOLOv11**

#### **Configuration Example (`data.yaml`)**
```yaml
train: ../Train/images
val: ../Valid/images
test: /Data/SeaDronesSee Object Detection v2/Uncompressed/Test

nc: 5
names: ['0', '1', '2', '3', '4']
```

#### **Training Steps**

##### **Individual Job Submission**
- Navigate to the respective split folder and run:
  ```bash
  sbatch schedule_yolo11.sh
  ```

##### **Batch Job Submission**
- Submit jobs for all splits:
  - Training:
    ```bash
    bash start_all.sh
    ```
  - Validation:
    ```bash
    bash start_all_val.sh
    ```
  - Testing:
    ```bash
    bash start_all_test.sh
    ```

#### **Results Conversion**
- Convert YOLO predictions to COCO JSON format:
  ```bash
  python yolo_to_json.py --path /path/to/outputs --output results.json
  ```

---

### **Faster R-CNN**

#### **Configuration Example (`data.yaml`)**
```yaml
CLASSES:
- __background__
- '1'
- '2'
- '3'
- '4'
- '5'
NC: 6
SAVE_VALID_PREDICTION_IMAGES: false
TRAIN_DIR_IMAGES: /Data/Faster-RCNN/Train/images
TRAIN_DIR_LABELS: /Data/Faster-RCNN/Train/annotations
VALID_DIR_IMAGES: /Data/Faster-RCNN/Valid/images
VALID_DIR_LABELS: /Data/Faster-RCNN/Valid/annotations
```

#### **Training Steps**

##### **Individual Job Submission**
- Navigate to the respective split folder and run:
  ```bash
  sbatch Train_RCNN.sh
  ```

##### **Batch Job Submission**
- Submit jobs for all splits:
  - Training:
    ```bash
    bash run_all_train.sh
    ```
  - Validation:
    ```bash
    bash run_all_val.sh
    ```
  - Testing:
    ```bash
    bash resume_all.sh
    ```

---


### **Batch Job Submission**

Batch job submission scripts automate the scheduling of training, validation, and testing tasks for all dataset splits:

- **YOLOv11**:
  - Training:
    ```bash
    bash start_all.sh
    ```
  - Validation:
    ```bash
    bash start_all_val.sh
    ```
  - Testing:
    ```bash
    bash start_all_test.sh
    ```

- **Faster R-CNN**:
  - Training:
    ```bash
    bash run_all_train.sh
    ```
  - Validation:
    ```bash
    bash run_all_val.sh
    ```
  - Testing:
    ```bash
    bash resume_all.sh
    ```

### **Individual Job Submission**

For fine-grained control, individual job scripts can also be run for specific splits:

- **YOLOv11**:
  ```bash
  sbatch schedule_yolo11.sh
  ```

- **Faster R-CNN**:
  ```bash
  sbatch Train_RCNN.sh
  ```

---

## Notes
- Ensure all paths and configurations are updated in the respective scripts and `data.yaml` files before running.
- Refer to the individual READMEs in the **YOLO11** and **Faster R-CNN** subfolders for detailed usage instructions.

For further assistance, refer to the [Ultralytics Documentation](https://docs.ultralytics.com) or [FasterRCNN PyTorch Training Pipeline Repository](https://github.com/sovit-123/fasterrcnn-pytorch-training-pipeline).
