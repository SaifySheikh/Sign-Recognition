import cv2
import os
import time
import tkinter as tk
from PIL import Image, ImageTk


symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

def capture_images(symbols):
    for symbol in symbols:
        symbol_folder = os.path.join(data_folder, str(symbol))
        if not os.path.exists(symbol_folder):
            os.makedirs(symbol_folder)
        
        print(f"Taking images for {symbol}")
        
        
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
            
            
            roi = frame[50:430, 150:550]  
            
            
            cv2.rectangle(frame, (150, 50), (550, 430), (0, 255, 0), 2)  

            frame_with_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_with_roi)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            
            
            image_path = os.path.join(symbol_folder, f"{symbol}_{i}.jpg")
            cv2.imwrite(image_path, roi)
            
           
            progress = (i + 1) * 100 // 60
            progress_label.config(text=f"Progress: {progress}%")
            
            
            elapsed_time = time.time() - start_time
            time_to_wait = max(0, 1 - elapsed_time)
            time.sleep(time_to_wait)
            
            root.update()  
        
        cap.release()
        root.destroy()
        print(f"Finished capturing images for {symbol}")
        time.sleep(5)  

capture_images(symbols)
