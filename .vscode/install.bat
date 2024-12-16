@echo off
echo Installing Video Player...

:: Install dependencies
pip install -r requirements.txt

:: Create executable
python build.py

:: Optional: Install to startup
dist\video_player.exe --install-startup

echo Installation complete!
pause