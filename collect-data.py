import cv2
import os
import time
import tkinter as tk
from PIL import Image, ImageTk

# List of symbols
symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create data folder if it doesn't exist
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Function to capture images for each symbol
def capture_images(symbols):
    for symbol in symbols:
        symbol_folder = os.path.join(data_folder, str(symbol))
        if not os.path.exists(symbol_folder):
            os.makedirs(symbol_folder)
        
        print(f"Taking images for {symbol}")
        
        # Set up camera feed window
        root = tk.Tk()
        root.title(f"Capture images for {symbol}")
        
        instruction_label = tk.Label(root, text=f"Capturing images for '{symbol}'")
        instruction_label.pack(padx=10, pady=10)
        
        progress_label = tk.Label(root, text="Progress: 0%")
        progress_label.pack(padx=10, pady=5)
        
        camera_label = tk.Label(root)
        camera_label.pack(padx=10, pady=10)
        
        cap = cv2.VideoCapture(0)
        
        for i in range(60):
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Define region of interest (ROI)
            roi = frame[50:430, 150:550]  # Increase ROI size from (50, 150) to (430, 550)
            
            # Draw green rectangle around ROI
            cv2.rectangle(frame, (150, 50), (550, 430), (0, 255, 0), 2)  # Adjusted ROI coordinates
            
            # Display camera feed with ROI
            frame_with_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_with_roi)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            
            # Save image
            image_path = os.path.join(symbol_folder, f"{symbol}_{i}.jpg")
            cv2.imwrite(image_path, roi)
            
            # Update progress label
            progress = (i + 1) * 100 // 60
            progress_label.config(text=f"Progress: {progress}%")
            
            # Calculate time to wait for the next image
            elapsed_time = time.time() - start_time
            time_to_wait = max(0, 1 - elapsed_time)
            time.sleep(time_to_wait)
            
            root.update()  # Update the Tkinter window
        
        cap.release()
        root.destroy()  # Close the Tkinter window
        print(f"Finished capturing images for {symbol}")
        time.sleep(5)  # Delay between capturing images for different symbols

# Capture images for each symbol
capture_images(symbols)
