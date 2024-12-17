import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QLabel, QMessageBox, QSystemTrayIcon, QMenu, QAction, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from cryptography.fernet import Fernet

# Encryption utilities
KEY_FILE = "key.key"
USER_FILE = "user_data.txt"

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

# Login Page
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("User  ID:")
        self.user_input = QLineEdit(self)
        self.label_pass = QLabel("Password:")
        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")

        layout.addWidget(self.label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)

    def login(self):
        user_id = self.user_input.text()
        password = self.pass_input.text()

        if os.path.exists(USER_FILE):
            with open(USER_FILE, "rb") as file:
                stored_data = file.read().split(b"\n")
                for line in stored_data:
                    if line:
                        stored_user_id, stored_password = line.split(b"|")
                        stored_user_id = decrypt_data(stored_user_id)
                        stored_password = decrypt_data(stored_password)

                        if user_id == stored_user_id and password == stored_password:
                            QMessageBox.information(self, "Login", "Login successful!")
                            self.close()
                            self.player = VideoPlayer()
                            self.player.show()
                            return

                QMessageBox.warning(self, "Login", "Invalid credentials!")
        else:
            QMessageBox.warning(self, "Login", "No registered user found!")

    def register(self):
        user_id = self.user_input.text()
        password = self.pass_input.text()

        if user_id and password:
            encrypted_user_id = encrypt_data(user_id)
            encrypted_password = encrypt_data(password)

            with open(USER_FILE, "ab") as file:  # Append mode
                file.write(encrypted_user_id + b"|" + encrypted_password + b"\n")

            QMessageBox.information(self, "Register", "Registration successful!")
        else:
            QMessageBox.warning(self, "Register", "Please fill in all fields!")

# Video Player
class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.load_button = QPushButton("Load Video ")
        self.skip_forward_button = QPushButton(">>")
        self.skip_backward_button = QPushButton("<<")

        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.load_button.clicked.connect(self.load_video)
        self.skip_forward_button.clicked.connect(self.skip_forward)
        self.skip_backward_button.clicked.connect(self.skip_backward)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.load_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.skip_forward_button)
        layout.addWidget(self.skip_backward_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.media_player.setVideoOutput(self.video_widget)

        # System Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setToolTip("Video Player - Hover for info")
        tray_menu = QMenu()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.media_player.play()  # Attempt to play the video immediately after loading

            # Check if the media is loaded successfully
            if self.media_player.mediaStatus() == QMediaPlayer.NoMedia:
                QMessageBox.warning(self, "Error", "Failed to load video. Please check the file format.")
            else:
                self.media_player.play()  # Play the video if loaded successfully

    def play_video(self):
        if self.media_player.mediaStatus() == QMediaPlayer.Loaded:
            self.media_player.play()
        else:
            QMessageBox.warning(self, "Error", "No video loaded. Please load a video first.")

    def pause_video(self):
        self.media_player.pause()

    def skip_forward(self):
        self.media_player.setPosition(self.media_player.position() + 5000)

    def skip_backward(self):
        self.media_player.setPosition(self.media_player.position() - 5000)

# Main Function
if __name__ == "__main__":
    generate_key()

    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())