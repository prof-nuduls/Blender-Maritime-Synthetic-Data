
# Faster R-CNN Subfolder
**Derick Miller**  
**Dept. of Electrical and Computer Engineering**  
**Stevens Institute of Technology**  
**AAI646 Final Project**  

---

## Overview

The `pre-train` and `only_Real` subfolders contain scripts, utilities, and configuration files for training, testing, validating, and fine-tuning Faster R-CNN models on the JARVIS HPC. These scripts enable seamless management of training pipelines and automate tasks such as resuming training, evaluating models, and converting annotations.

---

## File Descriptions

### **Training, Testing, and Validation Scripts**
- **`Train_RCNN.sh`**: Script for training Faster R-CNN models.
- **`resume_RCNN.sh`**: Script to resume training from the last checkpoint.
- **`Test_RCNN.sh`**: Script for predicting on the test dataset using the trained weights.
- **`Val_RCNN.sh`**: Script for validating the Faster R-CNN model on the validation dataset.

### **Helper Scripts**
- **`convert_annot.py`**: Converts predictions into the proper submission format for MACVi evaluation.
- **`convert_parallel.py`**: Converts YOLO TXT labels into VOC XML format, enabling Faster R-CNN compatibility.
- **`edit_all_train.py`**: Automates the creation of training shell scripts for different configurations.
- **`edit_all_val.py`**: Automates the creation of validation shell scripts for different configurations.
- **`edit_all_test.py`**: Automates the creation of test shell scripts for different configurations.
- **`edit_all_resume.py`**: Automates the creation of resume shell scripts for different configurations.

### **Automation Scripts**
- **`run_all_train.sh`**: Submits all training jobs for different configurations.
- **`run_all_val.sh`**: Submits all validation jobs for different configurations.
- **`run_all_test.sh`**: Submits all test jobs for different configurations.
- **`resume_all.sh`**: Submits all jobs to resume training for different configurations.

---

## Data Configuration

This implementation requires a `data.yaml` file for defining paths to datasets, class labels, and other metadata. The `data.yaml` file must be configured for each training setup. Below is an example configuration:

```yaml
TRAIN_DIR_IMAGES: /Data/Faster-RCNN/Train/images
TRAIN_DIR_LABELS: /Data/Faster-RCNN/Train/annotations
VALID_DIR_IMAGES: /Data/Faster-RCNN/Valid/images
VALID_DIR_LABELS: /Data/Faster-RCNN/Valid/annotations
CLASSES: ['0', '1', '2', '3', '4']
NC: 5
SAVE_VALID_PREDICTION_IMAGES: True
```



## Usage Instructions

1. **Training Faster R-CNN Models**:
   - Ensure the `data.yaml` file is correctly configured.
   - Run the `Train_RCNN.sh` script:
     ```bash
     sbatch Train_RCNN.sh
     ```

2. **Resuming Training**:
   - To resume training from the last checkpoint, run the `resume_RCNN.sh` script:
     ```bash
     sbatch resume_RCNN.sh
     ```

3. **Testing**:
   - Run predictions on the test dataset using `Test_RCNN.sh`:
     ```bash
     sbatch Test_RCNN.sh
     ```

4. **Validation**:
   - Validate the model on the validation dataset using `Val_RCNN.sh`:
     ```bash
     sbatch Val_RCNN.sh
     ```

5. **Automating Job Submission**:
   - Use `run_all_train.sh`, `run_all_val.sh`, `run_all_test.sh`, and `resume_all.sh` to submit multiple jobs for training, validation, testing, and resuming.

---

## Notes
- Ensure all paths in the scripts and `data.yaml` are properly configured before running.
- These scripts are designed for SLURM-managed HPC environments like JARVIS.

---

For additional details or troubleshooting, refer to the project’s main documentation.
