import os
import cv2
import matplotlib.pyplot as plt

# Base directory containing 'images' and 'labels' folders
base_dir = "F:/Derick/Project"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Class labels (you can customize this list based on your dataset)
class_labels = {
    0: "Swimmer",
    1: "Boat",
    2: "Jet Ski",
    3: "Life Preserver",
    4: "Buoy",
}

# Create output directory for visualized images
output_dir = os.path.join(base_dir, "visualized_images")
os.makedirs(output_dir, exist_ok=True)

# Function to parse YOLO labels
def parse_yolo_label(label_path, img_width, img_height):
    """Parse a YOLO label file and return bounding box coordinates."""
    boxes = []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1]) * img_width
            y_center = float(parts[2]) * img_height
            box_width = float(parts[3]) * img_width
            box_height = float(parts[4]) * img_height

            # Convert YOLO box to corner coordinates
            x_min = int(x_center - box_width / 2)
            y_min = int(y_center - box_height / 2)
            x_max = int(x_center + box_width / 2)
            y_max = int(y_center + box_height / 2)

            boxes.append((class_id, x_min, y_min, x_max, y_max))
    return boxes

# Function to display bounding boxes on an image
def draw_bounding_boxes(image_path, label_path, output_path):
    """Draw bounding boxes on an image and save the visualized image."""
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    img_height, img_width = image.shape[:2]

    # Parse the label file
    boxes = parse_yolo_label(label_path, img_width, img_height)

    # Draw bounding boxes and class labels
    for class_id, x_min, y_min, x_max, y_max in boxes:
        color = (0, 255, 0)  # Green for bounding boxes
        label = class_labels.get(class_id, f"Class {class_id}")
        
        # Draw the rectangle
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
        
        # Draw the class label
        cv2.putText(
            image,
            label,
            (x_min, y_min - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
        )

    # Save or display the result
    cv2.imwrite(output_path, image)
    print(f"Visualized image saved to: {output_path}")

# Process each image in the images folder
for image_name in os.listdir(images_dir):
    if not image_name.endswith((".jpg", ".png", ".jpeg")):
        continue

    # Construct paths
    image_path = os.path.join(images_dir, image_name)
    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_name)
    output_path = os.path.join(output_dir, image_name)

    # Check if the corresponding label file exists
    if not os.path.exists(label_path):
        print(f"Label file not found for image: {image_name}")
        continue

    # Draw bounding boxes on the image
    draw_bounding_boxes(image_path, label_path, output_path)

print("Processing completed!")
