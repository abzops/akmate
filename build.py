import os
import sys
import shutil
import subprocess

def run_command(command, error_msg):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(e)
        sys.exit(1)

def main():
    print("=== YT MP3 Downloader Windows Executable Builder ===")

    # 1. Ensure pyinstaller is installed
    try:
        import PyInstaller
        print("[OK] PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"], "Failed to install pyinstaller")

    # 2. Locate ffmpeg.exe
    ffmpeg_source = shutil.which("ffmpeg")
    if ffmpeg_source:
        print(f"[OK] Found FFmpeg on system path: {ffmpeg_source}")
        # Copy to local directory to package it
        local_ffmpeg = os.path.join(os.getcwd(), "ffmpeg.exe")
        if not os.path.exists(local_ffmpeg):
            print(f"Copying FFmpeg to project directory...")
            shutil.copy2(ffmpeg_source, local_ffmpeg)
    else:
        # Check if local ffmpeg.exe already exists
        if os.path.exists("ffmpeg.exe"):
            print("[OK] Found local ffmpeg.exe in the project directory.")
        else:
            print("[ERROR] FFmpeg was not found on your system path or project directory.")
            print("Please ensure FFmpeg is installed and added to your environment PATH, or copy 'ffmpeg.exe' into this project folder.")
            sys.exit(1)

    # 3. Clean up previous build files if they exist
    print("Cleaning up old builds...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    if os.path.exists("YT-MP3-Downloader.spec"):
        os.remove("YT-MP3-Downloader.spec")

    # 4. Build single-file executable using PyInstaller
    # --add-data: includes frontend assets (templates and static folders)
    # --add-binary: includes the ffmpeg.exe binary inside the executable
    print("Building standalone executable (this may take a minute)...")
    pyinstaller_cmd = (
        f'"{sys.executable}" -m PyInstaller --onefile --noconfirm '
        '--name "YT-MP3-Downloader" '
        '--add-data "templates;templates" '
        '--add-data "static;static" '
        '--add-binary "ffmpeg.exe;." '
        'app.py'
    )
    
    run_command(pyinstaller_cmd, "PyInstaller build failed")

    print("\n=============================================")
    print("SUCCESS! Standalone Windows executable built.")
    print("Location: " + os.path.abspath(os.path.join("dist", "YT-MP3-Downloader.exe")))
    print("=============================================")
    print("You can now move this .exe file anywhere and run it without any dependencies or python installed.")

if __name__ == "__main__":
    main()
