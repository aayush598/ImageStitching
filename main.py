import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import os
import numpy as np

# Global variables for bounding box selection
bbox = None
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0

def select_bbox(event, x, y, flags, param):
    """Handles mouse events for selecting the bounding box."""
    global x_start, y_start, x_end, y_end, cropping, bbox
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x, y
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        bbox = (min(x_start, x_end), min(y_start, y_end), abs(x_end - x_start), abs(y_end - y_start))
        print(f"Selected Bounding Box: {bbox}")
        messagebox.showinfo("Bounding Box Selected", f"Coordinates: {bbox}")
        cv2.destroyAllWindows()

def show_first_frame():
    """Displays the first frame of the video and lets the user select a bounding box."""
    global bbox

    cap = cv2.VideoCapture("video.mp4")
    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Cannot read video file")
        return

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.namedWindow("Select Bounding Box")
    cv2.setMouseCallback("Select Bounding Box", select_bbox)

    while True:
        temp_frame = frame.copy()
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Select Bounding Box", temp_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or bbox:
            break

    cv2.destroyAllWindows()

def extract_frames():
    """Extracts and crops frames based on the selected bounding box."""
    global bbox
    if bbox is None:
        messagebox.showerror("Error", "No bounding box selected")
        return

    video_path = "video.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open video file")
        return

    skip_frames = int(slider.get())
    frame_count = 0
    output_folder = "extracted_frames"
    os.makedirs(output_folder, exist_ok=True)

    x, y, width, height = bbox

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cropped_frame = frame[y:y+height, x:x+width]

        if frame_count % (skip_frames + 1) == 0:
            frame_filename = f"{output_folder}/frame_{frame_count:04d}.jpg"
            cv2.imwrite(frame_filename, cropped_frame)
            print(f"Saved: {frame_filename}")

        frame_count += 1

    cap.release()
    print("Frame extraction and cropping completed.")

def combine_images_horizontally():
    """Combines extracted frames into a single image."""
    input_folder = "extracted_frames"
    output_image = "combined_image.jpg"

    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))])
    if not image_files:
        print("No images found in the folder.")
        return

    images = [cv2.imread(os.path.join(input_folder, img)) for img in image_files]
    height = images[0].shape[0]
    images = [cv2.resize(img, (img.shape[1], height)) for img in images]
    combined_image = np.hstack(images)
    cv2.imwrite(output_image, combined_image)
    print(f"Saved combined image as {output_image}")

# GUI Setup
root = tk.Tk()
root.title("Video Processing Tool")

tk.Button(root, text="Select Bounding Box", command=show_first_frame).pack(pady=10)
tk.Label(root, text="Frames to Skip:").pack()
slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
slider.pack()
ttk.Button(root, text="Extract & Crop Frames", command=extract_frames).pack()
ttk.Button(root, text="Combine Images Horizontally", command=combine_images_horizontally).pack()

root.mainloop()
