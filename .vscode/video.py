import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import threading
import pystray
from pystray import MenuItem, Icon
from PIL import Image, ImageDraw, ImageTk
import time
import os
import sys
import argparse

class VideoPlayerApp:
    def __init__(self, start_in_tray=False):
        # Initialize without creating root window if starting in tray
        self.root = None if start_in_tray else tk.Tk()
        
        # Video Player Variables
        self.video_source = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = None
        self.video_thread = None
        self.frame_rate = 30  # Default frame rate
        self.current_frame_count = 0  # Track current frame count
        
        # System Tray Setup
        self.tray_icon = None
        self.setup_system_tray()
        
        # If not starting in tray, create UI
        if not start_in_tray:
            self.initialize_ui()

    def setup_system_tray(self):
        # Create System Tray Icon
        icon_image = self.create_tray_icon()
        menu = (
            MenuItem('Open Player', self.show_window),
            MenuItem('Load Video', self.load_video),
            MenuItem('Exit', self.exit_application)
        )
        self.tray_icon = pystray.Icon("Video Player", icon_image, "Video Player", menu)

    def create_tray_icon(self):
        # Create a colorful gradient tray icon
        width, height = 64, 64
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)

        # Create a gradient effect
        for i in range(height):
            color = (255 - int(255 * (i / height)), int(255 * (i / height)), 100)  # Gradient from red to green
            draw.line([(0, i), (width, i)], fill=color)

        # Add a border
        draw.rectangle([0, 0, width, height], outline="black", width=2)

        return image

    def initialize_ui(self):
        if self.root is None:
            self.root = tk.Tk()
        
        self.root.title("Advanced Video Player")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')

        # Create UI Components
        self.create_ui_components()
        
        # Set up close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def create_ui_components(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Video Canvas
        self.canvas = tk.Canvas(main_frame, width=640, height=480, bg='black')
        self.canvas.pack(pady=10)

        # Control Frame
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(pady=10)

        # Buttons
        btn_style = {
            'bg': '#34495e', 
            'fg': 'white', 
            'activebackground': '#2980b9', 
            'font': ('Arial', 10)
        }

        buttons = [
            ("Load Video", self.load_video),
            ("Play", self.play_video),
            ("Pause", self.pause_video),
            ("Stop", self.stop_video),
            ("Skip Backward", self.skip_backward),
            ("Skip Forward", self.skip_forward)
        ]

        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command, **btn_style)
            btn.pack(side=tk.LEFT, padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(main_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, 
                                     length=600, 
                                     variable=self.progress_var,
                                     bg='#34495e')
        self.progress_bar.pack(pady=10)

    def load_video(self, icon=None, item=None):
        # Ensure we have a root window
        if self.root is None:
            self.initialize_ui()
            self.show_window()

        # Close the system tray menu if opened from tray
        if icon:
            icon.stop()

        # Open file dialog
        self.video_source = filedialog.askopenfilename(
            title="Select Video File", 
            filetypes=[("Video Files ", "*.mp4;*.avi;*.mov;*.mkv")]
        )
        if self.video_source:
            self.current_frame_count = 0
            self.is_playing = False
            self.is_paused = False
            self.play_video()

    def play_video(self):
        if self.video_source and not self.is_playing:
            self.is_playing = True
            self.video_thread = threading.Thread(target=self.video_loop)
            self.video_thread.start()

    def video_loop(self):
        cap = cv2.VideoCapture(self.video_source)
        while self.is_playing:
            if not self.is_paused:
                ret, frame = cap.read()
                if not ret:
                    break
                self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame_count += 1 
                self.update_canvas()
                time.sleep(1 / self.frame_rate)
        cap.release()

    def update_canvas(self):
     if self.current_frame is not None:
        img = Image.fromarray(self.current_frame)
        img = img.resize((640, 480), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.update_progress()

    def update_progress(self):
        if self.video_source:
            total_frames = int(cv2.VideoCapture(self.video_source).get(cv2.CAP_PROP_FRAME_COUNT))
            self.progress_var.set((self.current_frame_count / total_frames) * 100)

    def pause_video(self):
        self.is_paused = not self.is_paused

    def stop_video(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.join()
        self.current_frame_count = 0
        self.progress_var.set(0)

    def skip_backward(self):
        self.current_frame_count = max(0, self.current_frame_count - 10)  # Skip back 10 frames

    def skip_forward(self):
        self.current_frame_count += 10  # Skip forward 10 frames

    def minimize_to_tray(self):
        self.root.withdraw()
        self.tray_icon.run()

    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        if icon:
            icon.stop()

    def exit_application(self, icon=None, item=None):
        self.stop_video()
        if icon:
            icon.stop()
        sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Video Player")
    parser.add_argument('--tray', action='store_true', help="Start in system tray")
    args = parser.parse_args()

    app = VideoPlayerApp(start_in_tray=args.tray)
    if not args.tray:
        app.root.mainloop()

