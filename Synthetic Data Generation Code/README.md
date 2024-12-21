# Synthetic Data Generation Code
**Derick Miller**  
**Dept. of Electrical and Computer Engineering**  
**Stevens Institute of Technology**  
**AAI646 Final Project**  

This folder contains all the necessary scripts and utilities for generating a synthetic dataset using Blender. The generated dataset is designed to supplement real-world data in training object detection models for maritime search and rescue (SAR) applications.

---

## Overview of Files

### **1. `synthetic_data_generation_1080.py`**
This script generates synthetic data using Blender with a focus on 1080p resolution. It loads predefined lake models, places objects randomly, calculates bounding boxes, and exports images along with YOLO-compatible label files. It accepts `--start` and `--end` arguments to specify the range of images to generate.

### **2. `synthetic_data_generation_4k.py`**
Similar to `synthetic_data_generation_1080.py`, but generates synthetic data with a 4K resolution. 

### **3. `parallel_execution.py`**
This script facilitates parallel execution of the synthetic data generation process. It divides the total number of images into chunks and runs multiple instances of Blender simultaneously, significantly speeding up the dataset creation process.

### **4. `verify_labels.py`**
A utility script for verifying the accuracy of generated labels. It overlays bounding boxes on the corresponding images and saves the visualized outputs, enabling users to inspect the quality of the generated data.

---

## Getting Started

### **Requirements**
- **Blender 4.2** installed on your system.
- Python 3.6 or later with the required libraries specified in the main project’s `requirements.txt`.

### **Steps to Generate Synthetic Data**
1. **Set Up Blender Assets**:
   - Ensure that all `.blend` files and asset libraries (e.g., models for swimmers, boats, etc.) are placed in the correct paths as specified in the scripts.

2. **Run the Data Generation Script**:
   - Use `synthetic_data_generation_1080.py` for 1080p images or `synthetic_data_generation_4k.py` for 4K images.
   - Example command:
     ```bash
     blender --background --python synthetic_data_generation_1080.py -- --start=0 --end=100
     ```

3. **Parallelize the Process**:
   - Use `parallel_execution.py` to distribute the workload across multiple processes.
   - Example command:
     ```bash
     python parallel_execution.py
     ```

4. **Verify the Generated Labels**:
   - After generation, run `verify_labels.py` to inspect the bounding boxes on the images.
   - Example command:
     ```bash
     python verify_labels.py
     ```

---

## Folder Structure
Ensure your workspace is organized as follows:
```
Synthetic_Data_Generation_Code/
   ├── synthetic_data_generation_1080.py
   ├── synthetic_data_generation_4k.py 
   ├── parallel_execution.py
   ├── verify_labels.py  

Lake_Models/ 
   ├── Lake.blend
   ├── Lake_with_sky.blend
   ├── Lake_with_sky_1080.blend 

Assets/ 
   ├── swimmer_1.blend
   ├── boat_1.blend
   └── ... 


   ```


---

## Example Commands

### Generate 500 images at 1080p resolution:
```bash
blender --background --python synthetic_data_generation_1080.py -- --start=0 --end=500
```
### Generate 1,000 images in parallel:
```bash
python parallel_execution.py
```
### Verify labels on generated images:
```bash
python verify_labels.py
```