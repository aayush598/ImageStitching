import cv2
import tkinter as tk
from tkinter import ttk
import os

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

# GUI Setup
root = tk.Tk()
root.title("Frame Extractor & Cropper")

# Slider
tk.Label(root, text="Frames to Skip:").pack()
slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
slider.pack()

# Extract Button
extract_button = ttk.Button(root, text="Extract & Crop Frames", command=extract_frames)
extract_button.pack()

# Run GUI
root.mainloop()
