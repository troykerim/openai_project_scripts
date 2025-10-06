'''
    Used only for displaying the XML bounding boxes to check if they match image.
'''

import os
import cv2
import matplotlib.pyplot as plt


image_path = r""
bbox_txt_path = r""

# Looading an image
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

# reading file
boxes = []
with open(bbox_txt_path, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        label, xmin, xmax, ymin, ymax = parts
        boxes.append((label, int(xmin), int(xmax), int(ymin), int(ymax)))

# Creating Bounding Boxes
image_with_boxes = image.copy()
for label, xmin, xmax, ymin, ymax in boxes:
    cv2.rectangle(image_with_boxes, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)  # Blue boxes (BGR)
    cv2.putText(image_with_boxes, label, (xmin, ymin - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Display figures
plt.figure(figsize=(8, 6))
plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
file_name = os.path.basename(image_path)
plt.title(f"Bounding Boxes for: {file_name}", fontsize=10)
plt.axis("off")
plt.tight_layout()
plt.show()