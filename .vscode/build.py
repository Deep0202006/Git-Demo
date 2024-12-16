import PyInstaller.__main__
import sys
import os

# Ensure icon is in the same directory
ICON_PATH = 'video_player_icon.ico'  # Create this icon

def create_exe():
    # PyInstaller arguments
    pyinstaller_args = [
        '--onefile',  # Single executable
        '--windowed',  # No console window
        f'--icon={ICON_PATH}',  # Application icon
        '--add-data=video_player_icon.ico:.',  # Include icon in package
        'video_player.py'  # Your main script
    ]
    
    # Build the executable
    PyInstaller.__main__.run(pyinstaller_args)

def main():
    create_exe()
    print("Build completed successfully!")

if __name__ == "__main__":
    main()