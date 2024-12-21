# Blender-Maritime-Synthetic-Data
**Derick Miller**  
**Dept. of Electrical and Computer Engineering**  
**Stevens Institute of Technology**  
**AAI646 Final Project**  

---

## Blender Synthetic Data Generation for Maritime Search and Rescue Object Detection

This repository provides all necessary resources for generating synthetic datasets using Blender, training object detection models, and evaluating their performance for maritime search and rescue (SAR) applications. The project aims to address the challenge of limited real-world training data by leveraging synthetic data to improve model accuracy and robustness.

This project is specifically designed for Stevens researchers utilizing the JARVIS HPC cluster but can be adapted for use on any SLURM-managed server or HPC environment for model training.

---

## Project Structure

### **1. Lake Models**
This folder contains Blender `.blend` files used to create realistic lake environments:
- **`Lake.blend`**: A simple lake model for quick setups.
- **`Lake_with_sky_1080.blend`**: A detailed lake environment with 1080p resolution and realistic sky textures.
- **`Lake_with_sky.blend`**: A high-resolution lake model (4K) with advanced sky and environmental effects.

### **2. Synthetic Data Generation Code**
This folder includes all scripts and utilities needed for generating synthetic images and annotations. Detailed instructions for usage can be found within the folder.

### **3. Model Training Code**
This folder contains all resources and scripts required for training object detection models on the JARVIS HPC or any SLURM-managed environment. Refer to the folder for specific details on configuration and execution.

---

## Getting Started

### **Requirements**
- **Blender 4.2**: For synthetic data generation.
- **JARVIS HPC Access** (or equivalent SLURM-managed server): For model training and testing.
- **Dependencies**: Install required Python libraries using `pip install -r requirements.txt`.

### **Recommened Hardware**  
- **RTX or Equivalent GPU** : For sythetic data generation, and model training.

### **Steps**
1. **Generate Synthetic Data**:
   - Follow the instructions in the `Synthetic Data Generation Code` Folder.
   - Run the appropriate script from the README.md to create images and annotations.
   - Parallelize data generation as needed for large-scale tasks.

2. **Prepare Datasets**:
   - Download the SeaDroneSee dataset from the MACVi website.
   - Convert JSON labels to YOLO TXT format using the provided scripts.

3. **Train Models**:
   - Follow instructions in `Model Training Code` folder.
   - Update YAML configuration files for training paths.
   - Use the scripts in the `Model Training Code` folder to schedule training jobs on SLURM-managed servers.

4. **Evaluate Results**:
   - Convert prediction outputs to the appropriate submission format using the scripts provided.
   - Submit results to MACVi for evaluation.

---