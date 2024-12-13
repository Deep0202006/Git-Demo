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
        # Create a custom tray icon
        width, height = 64, 64
        image = Image.new('RGB', (width, height), color='#3498db')
        dc = ImageDraw.Draw(image)
        dc.rectangle([10, 10, width-10, height-10], fill='#2980b9')
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
            ("Stop", self.stop_video)
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
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )
        
        if self.video_source:
            messagebox.showinfo("Video Loaded", f"Loaded: {os.path.basename(self.video_source)}")

    def play_video(self):
        if not self.video_source:
            messagebox.showwarning("Warning", "Please load a video first!")
            return

        if self.is_paused:
            self.is_paused = False
            return

        self.is_playing = True
        self.video_thread = threading.Thread(target=self.video_playback)
        self.video_thread.start()

    def video_playback(self):
        cap = cv2.VideoCapture(self.video_source)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame_count = 0

        while self.is_playing:
            if self.is_paused:
                time.sleep(0.1)
                continue

            ret, frame = cap.read()
            if not ret:
                break

            current_frame_count += 1
            progress = (current_frame_count / total_frames) * 100
            self.progress_var.set(progress)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            self.display_frame(frame)

            time.sleep(1/30)  # Control frame rate

        cap.release()
        self.is_playing = False

    def display_frame(self, frame):
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def pause_video(self):
        self.is_paused = not self.is_paused

    def stop_video(self):
        self.is_playing = False
        self.is_paused = False
        self.progress_var.set(0)

    def show_window(self, icon=None, item=None):
        # Ensure UI is initialized
        if self.root is None:
            self.initialize_ui()
        
        # Bring window to front
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        # Stop tray icon if opened from tray
        if icon:
            icon.stop()

    def minimize_to_tray(self):
        if self.root:
            self.root.withdraw()
        
        # Restart tray icon if not running
        if self.tray_icon:
            self.tray_icon.run()

    def exit_application(self, icon=None, item=None):
        # Stop video playback
        self.is_playing = False
        
        # Stop tray icon
        if icon:
            icon.stop()
        
        # Quit application
        if self.root:
            self.root.quit()
        
        # Exit completely
        sys.exit(0)

    def run(self):
        # If root exists, start mainloop
        if self.root:
            # Start system tray in a separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run)
            tray_thread.start()
            
            # Start main UI loop
            self.root.mainloop()
        else:
            # If no root (started from tray), just run tray icon
            self.tray_icon.run()

def parse_arguments():
    """Parse comman d-line arguments."""
    parser = argparse.ArgumentParser(description="Advanced Video Player")
    parser.add_argument('--tray', action='store_true', help="Start the application in the system tray")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    app = VideoPlayerApp(start_in_tray=args.tray)
    app.run() 