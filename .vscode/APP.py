import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import threading
import pystray
from pystray import MenuItem, Icon
from PIL import Image, ImageDraw, ImageTk
import os
import time
import argparse
import requests
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from datetime import datetime

# Encryption utilities
KEY_FILE = "key.key"
USER_FILE = "user_data.txt"
API_URL = "http://127.0.0.1:5000"  # URL for the Flask API

# Flask app for tracking login/logout times
app = Flask(__name__)
user_sessions = {}

@app.route('/login', methods=['POST'])  
def login():
    data = request.json
    user_id = data.get('user_id')
    login_time = datetime.now().isoformat()
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'login_time': login_time, 'logout_time': None, 'total_time': 0}
    else:
        user_sessions[user_id]['login_time'] = login_time
    
    return jsonify({"message": "Login time recorded", "data": user_sessions[user_id]}), 200

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    user_id = data.get('user_id')
    logout_time = datetime.now().isoformat()
    
    if user_id in user_sessions:
        user_sessions[user_id]['logout_time'] = logout_time
        login_time = datetime.fromisoformat(user_sessions[user_id]['login_time'])
        logout_time_dt = datetime.fromisoformat(logout_time)
        total_time = (logout_time_dt - login_time).total_seconds()
        user_sessions[user_id]['total_time'] += total_time
    
    return jsonify({"message": "Logout time recorded", "data": user_sessions[user_id]}), 200

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(user_sessions), 200

def run_flask_app():
    app.run(port=5000)

# Start Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.daemon = True  # Allow thread to exit when the main program exits
flask_thread.start()

# Encryption functions
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as file:
        return file.read()

def encrypt_data(data):
    f = Fernet(load_key())
    return f.encrypt(data.encode())

def decrypt_data(data):
    f = Fernet(load_key())
    return f.decrypt(data).decode()

# Login Window
class LoginWindow(tk.Toplevel):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.title("Login")
        self.geometry("300x200")
        self.configure(bg="#34495e")

        tk.Label(self, text="User  ID:", bg="#34495e", fg="white").pack(pady=5)
        self.user_entry = tk.Entry(self)
        self.user_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#34495e", fg="white").pack(pady=5)
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)
        
        tk.Button(self, text="Login", command=self.login, bg="#2980b9", fg="white").pack(pady=5)
        tk.Button(self, text="Register", command=self.register, bg="#27ae60", fg="white").pack(pady=5)

    def login(self):
        user_id = self.user_entry.get()
        password = self.pass_entry.get()

        if os.path.exists(USER_FILE):
            with open(USER_FILE, "rb") as file:
                stored_data = file.read().split(b"\n")
                for line in stored_data:
                    if line:
                        stored_user_id, stored_password = line.split(b"|")
                        stored_user_id = decrypt_data(stored_user_id)
                        stored_password = decrypt_data(stored_password)

                        if user_id == stored_user_id and password == stored_password:
                            messagebox.showinfo("Login", "Login successful!")
                            self.on_login_success()
                            # Send login time to the API
                            requests.post(f"{API_URL}/login", json={"user_id": user_id})
                            self.destroy()
                            return
                messagebox.showwarning("Login", "Invalid credentials!")
        else:
            messagebox.showwarning("Login", "No registered user found!")

    def register(self):
        user_id = self.user_entry.get()
        password = self.pass_entry.get()

        if user_id and password:
            encrypted_user_id = encrypt_data(user_id)
            encrypted_password = encrypt_data(password)

            with open(USER_FILE, "ab") as file:  # Append mode
                file.write(encrypted_user_id + b"|" + encrypted_password + b"\n")

            messagebox.showinfo("Register", "Registration successful!")
        else:
            messagebox.showwarning("Register", "Please fill in all fields!")

# Video Player App
class VideoPlayerApp:
    def __init__(self, start_in_tray=False):
        self.root = None if start_in_tray else tk.Tk()
        self.video_source = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = None
        self.video_thread = None
        self.frame_rate = 30
        self.current_frame_count = 0
        
        self.tray_icon = None
        self.setup_system_tray()

        if not start_in_tray:
            self.check_and_create_default_user()
            self.show_login()

    def check_and_create_default_user(self):
        if not os.path.exists(USER_FILE):
            # Create default user credentials
            default_user_id = "admin"
            default_password = "ecs@2021"
            encrypted_user_id = encrypt_data(default_user_id)
            encrypted_password = encrypt_data(default_password)

            with open(USER_FILE, "ab") as file: 
                file.write(encrypted_user_id + b"|" + encrypted_password + b"\n")
            messagebox.showinfo("Registration", "Default user created!")

    def setup_system_tray(self):
        icon_image = self.create_tray_icon()
        menu = (
            MenuItem('Open Player', self.show_window),
            MenuItem('Load Video', self.load_video),
            MenuItem('View User Sessions', self.view_user_sessions),
            MenuItem('Exit', self.exit_application)
        )
        self.tray_icon = pystray.Icon("Video Player", icon_image, "Video Player", menu)
        self.tray_icon.tooltip = "Video Player"  # Set the tooltip
        self.tray_icon.run()  # Run the tray icon immediately

    def create_tray_icon(self):
        width, height = 64, 64
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)

        for i in range(height):
            color = (255 - int(255 * (i / height)), int(255 * (i / height)), 100)
            draw.line([(0, i), (width, i)], fill=color)

        draw.rectangle([0, 0, width, height], outline="black", width=2)
        return image

    def show_login(self):
        self.login_window = LoginWindow(self.root, self.initialize_ui)
        self.root.withdraw()

    def initialize_ui(self):
        if self.root is None:
            self.root = tk.Tk()

        self.root.deiconify()
        self.root.title("Advanced Video Player")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')

        self.create_ui_components()
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def create_ui_components(self):
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(main_frame, width=640, height=480, bg='black')
        self.canvas.pack(pady=10)

        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(pady=10)

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

        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(main_frame, from_=0, to=100,
                                     orient=tk.HORIZONTAL,
                                     length=600,
                                     variable=self.progress_var,
                                     bg='#34495e')
        self.progress_bar.pack(pady=10)

        self.api_data_text = tk.Text(main_frame, height=10, bg='#34495e', fg='white')
        self.api_data_text.pack(pady=10, padx=10)

    def load_video(self):
        self.video_source = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
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
                self.current_frame_count += 1
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((640, 480))
                self.current_frame = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
                self.progress_var.set((self.current_frame_count / cap.get(cv2.CAP_PROP_FRAME_COUNT)) * 100)
                time.sleep(1 / self.frame_rate)
        cap.release()

    def pause_video(self):
        self.is_paused = not self.is_paused

    def stop_video(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.join()
        self.current_frame_count = 0
        self.canvas.delete("all")  

    def skip_backward(self):
        self.current_frame_count = max(0, self.current_frame_count - 10)  # Skip back 10 frames

    def skip_forward(self):
        self.current_frame_count += 10  # Skip forward 10 frames

    def minimize_to_tray(self):
        self.root.withdraw()

    def show_window(self):
        self.tray_icon.stop()
        self.root.deiconify()

    def exit_application(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.join()
        # Send logout time to the API
        user_id = self.login_window.user_entry.get()  # Assuming user_id is stored here
        requests.post(f"{API_URL}/logout", json={"user_id": user_id})
        self.tray_icon.stop()
        self.root.quit()

    def view_user_sessions(self):
    # Check if api_data_text is initialized
     if not hasattr(self, 'api_data_text'):
        messagebox.showwarning("Warning", "User  sessions are not available yet. Please log in first.")
        return  # Exit the method if api_data_text is not initialized
# Make a request to get user sessions
    response = requests.get(f"{API_URL}/sessions")
    if response.status_code == 200:
        sessions = response.json()
        self.api_data_text.delete(1.0, tk.END)  # Clear previous text
    for user_id, data in sessions.items():
        self.api_data_text.insert(tk.END, f"User  ID: {user_id}\n")
        self.api_data_text.insert(tk.END, f"Login Time: {data['login_time']}\n")
        self.api_data_text.insert(tk.END, f"Logout Time: {data['logout_time']}\n")
        self.api_data_text.insert(tk.END, f"Total Time Spent: {data['total_time']} seconds\n\n")
    else:
        messagebox.showerror("Error", "Failed to retrieve user sessions.")

if __name__ == "__main__":
    generate_key()
    parser = argparse.ArgumentParser(description="Advanced Video Player")
    parser.add_argument('--tray', action='store_true', help="Start in system tray")
    args = parser.parse_args()

    app = VideoPlayerApp(start_in_tray=args.tray)
    if not args.tray:
        app.root.mainloop()

