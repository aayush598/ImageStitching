import cv2
import tkinter as tk
from tkinter import ttk
import os

# Function to extract frames
def extract_frames():
    video_path = "video.mp4"  # Change path if needed
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video file")
        return
    
    skip_frames = int(slider.get())  # Get skip value from slider
    frame_count = 0

    # Create output folder if needed
    output_folder = "extracted_frames"
    os.makedirs(output_folder, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate frame 90 degrees anti-clockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Save frame if it meets the skip condition
        if frame_count % (skip_frames + 1) == 0:
            frame_filename = f"{output_folder}/frame_{frame_count:04d}.jpg"  # 4-digit format
            cv2.imwrite(frame_filename, frame)
            print(f"Saved: {frame_filename}")

        frame_count += 1

    cap.release()
    print("Frame extraction completed.")

# GUI Setup
root = tk.Tk()
root.title("Frame Extractor")

# Slider
tk.Label(root, text="Frames to Skip:").pack()
slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
slider.pack()

# Extract Button
extract_button = ttk.Button(root, text="Extract Frames", command=extract_frames)
extract_button.pack()

# Run GUI
root.mainloop()
