import cv2
import tkinter as tk
from tkinter import ttk
import os
import numpy as np

# Function to extract and crop frames
def extract_frames():
    video_path = "video.mp4"  # Change if needed
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video file")
        return
    
    skip_frames = int(slider.get())  # Get skip value from slider
    frame_count = 0

    # Create output folder
    output_folder = "extracted_frames"
    os.makedirs(output_folder, exist_ok=True)

    # Cropping coordinates
    x, y, width, height = 160, 0, 220, 640

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate frame 90 degrees anti-clockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Crop the frame using the given bounding box
        cropped_frame = frame[y:y+height, x:x+width]

        # Save frame if it meets the skip condition
        if frame_count % (skip_frames + 1) == 0:
            frame_filename = f"{output_folder}/frame_{frame_count:04d}.jpg"  # 4-digit format
            cv2.imwrite(frame_filename, cropped_frame)
            print(f"Saved: {frame_filename}")

        frame_count += 1

    cap.release()
    print("Frame extraction and cropping completed.")

# Function to combine images horizontally
def combine_images_horizontally():
    input_folder = "extracted_frames"
    output_image = "combined_image.jpg"

    # Get sorted list of image files
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))])

    # Check if images exist
    if not image_files:
        print("No images found in the folder.")
        return

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

# GUI Setup
root = tk.Tk()
root.title("Frame Extractor & Image Combiner")

# Slider for skipping frames
tk.Label(root, text="Frames to Skip:").pack()
slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
slider.pack()

# Extract Button
extract_button = ttk.Button(root, text="Extract & Crop Frames", command=extract_frames)
extract_button.pack()

# Combine Button
combine_button = ttk.Button(root, text="Combine Images Horizontally", command=combine_images_horizontally)
combine_button.pack()

# Run GUI
root.mainloop()
