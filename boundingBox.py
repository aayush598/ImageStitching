import cv2
import tkinter as tk
from tkinter import messagebox

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

    # Load the first frame of the video
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
        if key == 27 or bbox:  # Press ESC or select a bounding box to exit
            break

    cv2.destroyAllWindows()

# Tkinter GUI
root = tk.Tk()
root.title("Bounding Box Selector")

select_button = tk.Button(root, text="Select Bounding Box", command=show_first_frame)
select_button.pack(pady=20)

root.mainloop()
