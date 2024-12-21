# YOLO11 and Only_Real Subfolders
**Derick Miller**  
**Dept. of Electrical and Computer Engineering**  
**Stevens Institute of Technology**  
**AAI646 Final Project**  

---

## Overview

The `pre-train` and `only_real` subfolders contain scripts, shell files, and utilities for training, testing, validating, and fine-tuning YOLOv11 models on the JARVIS HPC. These scripts are designed to streamline the workflow for running various configurations and automating tasks such as training, resuming from checkpoints, evaluating models, and exporting predictions. 

The implementation in this project is based on the official Ultralytics YOLOv11 documentation.

---
## Data Configuration

This implementation relies on `data.yaml` files for defining paths to datasets, class labels, and other metadata required for training, validation, and testing. A `data.yaml` file must be created for all models trained in this project. For more information about `data.yaml` configurations, refer to the [Ultralytics Documentation](https://docs.ultralytics.com).


### **Example `data.yaml` File**
Below is an example of the `data.yaml` configuration file used in this project:
```yaml
train: ../Train/images
val: ../Valid/images
test: ../SeaDronesSee Object Detection v2/Uncompressed Version/Test


nc: 5
names: ['0', '1', '2', '3', '4']
```
## File Descriptions

### **Training and Testing Scripts**
- **`yolo11.sh`**: Main script for training YOLOv11 models, handling both training and validation.
- **`yolo11_fine_tune.sh`**: Script for fine-tuning YOLOv11 using pretrained weights.
- **`yolo11_resume.sh`**: Resumes training from the last checkpoint.
- **`yolo11_test.sh`**: Predicts on test data using the best-trained weights and exports results.
- **`yolo11_val.sh`**: Validates the YOLOv11 model on the validation dataset.

---

### **Scheduling Scripts**
These shell scripts are configured to work with SLURM on the JARVIS HPC for scheduling jobs:
- **`schedule_yolo11.sh`**: Schedules YOLOv11 training jobs.
- **`schedule_yolo_Fine_tune.sh`**: Schedules fine-tuning jobs for YOLOv11.
- **`schedule_yolo_resume.sh`**: Schedules jobs to resume training.
- **`schedule_yolo_test.sh`**: Schedules test jobs for YOLOv11.
- **`schedule_yolo_val.sh`**: Schedules validation jobs for YOLOv11.

---

### **Helper Scripts**
- **`start_all.sh`**: Automates the submission of all YOLOv11 training jobs across different configurations.
- **`start_all_resume.sh`**: Automates the resumption of all training jobs from checkpoints.
- **`start_all_test.sh`**: Automates the submission of test jobs.
- **`start_all_val.sh`**: Automates the submission of validation jobs.

---

## Usage Instructions

1. **Training YOLOv11 Models**:
   - Run the `schedule_yolo11.sh` script to schedule a training job:
     ```bash
     sbatch schedule_yolo11.sh
     ```

2. **Fine-Tuning with Pretrained Weights**:
   - Use the `schedule_yolo_Fine_tune.sh` script to schedule fine-tuning:
     ```bash
     sbatch schedule_yolo_Fine_tune.sh
     ```

3. **Resuming Training**:
   - To resume from the last checkpoint, schedule `schedule_yolo_resume.sh`:
     ```bash
     sbatch schedule_yolo_resume.sh
     ```

4. **Testing**:
   - Schedule predictions on the test dataset using `schedule_yolo_test.sh`:
     ```bash
     sbatch schedule_yolo_test.sh
     ```

5. **Validation**:
   - Validate the model on the validation dataset using `schedule_yolo_val.sh`:
     ```bash
     sbatch schedule_yolo_val.sh
     ```

6. **Automating Job Submission**:
   - Use the `start_all.sh`, `start_all_resume.sh`, `start_all_test.sh`, and `start_all_val.sh` scripts to submit multiple jobs at once.

---

This README applies to both subfolders. Adjust file paths and parameters as necessary for your specific configurations.
