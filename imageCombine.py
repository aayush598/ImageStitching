import cv2
import os
import numpy as np

# Folder containing extracted frames
input_folder = "extracted_frames"
output_image = "combined_image.jpg"

# Get sorted list of image files
image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))])

# Check if images are found
if not image_files:
    print("No images found in the folder.")
    exit()

# Read all images
images = [cv2.imread(os.path.join(input_folder, img)) for img in image_files]

# Ensure all images have the same height
height = images[0].shape[0]
images = [cv2.resize(img, (img.shape[1], height)) for img in images]

# Concatenate images horizontally
combined_image = np.hstack(images)

# Save the combined image
cv2.imwrite(output_image, combined_image)
print(f"Saved combined image as {output_image}")
