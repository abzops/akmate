# 🎵 YT MP3 — YouTube to 320kbps MP3 Downloader

A premium, high-performance web application and standalone Windows utility that converts YouTube videos into high-quality **320kbps MP3** files in seconds. 

Built with **Flask**, **yt-dlp**, and **FFmpeg**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🎵 **320kbps MP3** — Full quality audio extraction.
- ⚡ **Turbo-Charged Speeds** — Multi-threaded segment downloads and fast LAME encoding.
- 📋 **Paste & Go** — Quick-paste button for clipboard URLs.
- 🖼️ **Rich Metadata** — Auto-embeds high-res video thumbnails, channel name, and title directly into the MP3 ID3 tags.
- 🎨 **Premium Glassmorphic UI** — Modern, dark-themed responsive user interface.
- 🛡️ **Bot Detection Bypass** — Secure cookies injection framework to bypass YouTube bot checks.
- 🖥️ **Windows Portable (.exe)** — Single-file portable app running in the background with zero local configuration.

---

## ⚡ Speed & Performance Optimizations

To ensure song conversions finish in **under 10 seconds**, the following settings are pre-configured:
1. **Parallel Downloads**: Downloads DASH/HLS audio segments using **8 concurrent threads** (up to 5x faster than single thread).
2. **Reduced Query Latency**: Disables manifest file lookups and format checks when requesting metadata.
3. **FFmpeg Turbo Mode**: Configured FFmpeg to use LAME's **fastest compression preset (`-compression_level 9`)** and enabled **automatic CPU multi-threading (`-threads 0`)**, cutting conversion times in half.

---

## 💻 Windows Standalone Executable (.exe)

You can run this application locally on Windows without installing Python, Flask, or FFmpeg:

1. Locate the pre-built executable:
   📁 `dist/YT-MP3-Downloader.exe`
2. **Double-click to Run**:
   - The application will run silently in the background (no command prompt window).
   - It will automatically open your default browser (Chrome, Edge, or Firefox) to `http://127.0.0.1:5000` showing the interface.
   - It includes a bundled `ffmpeg.exe` inside it, requiring no local setup.

### How to Re-compile the .exe:
To rebuild the executable yourself:
```bash
# Refresh/install PyInstaller and Pillow dependencies
pip install pyinstaller Pillow

# Run the automated build script
python build.py
```
The compiled output is saved directly to `dist/YT-MP3-Downloader.exe`.

---

## 🛡️ Bypassing YouTube Bot Check (Cookies Setup)

YouTube heavily throttles or blocks automated traffic (especially on hosted platforms like Render or VPNs). If you see the message *"Sign in to confirm you're not a bot"*, resolve it by injecting your browser session cookies:

### 1. Export Browser Cookies
1. Install a cookie exporter browser extension:
   - Chrome/Edge/Brave: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/ccjhcggmhmjiaobkcapjhhfgiejihfkd)
   - Firefox: [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
2. Log into [YouTube.com](https://www.youtube.com).
3. Open the extension and click **Export** to download a text file. Rename it to `cookies.txt`.

### 2. Apply Cookies
* **For Local Executable / Local Server**: 
  Place `cookies.txt` in the **same folder** as the `YT-MP3-Downloader.exe` (or in the root folder of this project). The app will automatically detect and apply it.
* **For Render.com Hosting**:
  Do not push cookies to GitHub. Instead, open your **Render Dashboard ➔ Web Service ➔ Environment**, add a variable with Key: `YOUTUBE_COOKIES`, and paste the entire text contents of your `cookies.txt` file as the Value.

---

## 🚀 Local Server Installation (Optional)

### Setup
```bash
# Clone the repository
git clone https://github.com/abzops/akmate.git
cd akmate

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 🌐 Deploy to Render (Free Tier hosting)

This repository includes a `render.yaml` blueprint and a `Dockerfile` for easy, free cloud hosting:

1. Push this code to a GitHub repository.
2. Sign in to [Render.com](https://render.com) using your GitHub account.
3. Click **New ➔ Web Service** and link your repository.
4. Render will read the `Dockerfile` and compile Python 3.11 with FFmpeg automatically.
5. Click **Create Web Service**.

---

## ⚖️ Rights, Disclaimer, and Terms of Use

### ⚠️ Legal Disclaimer
This software is intended **strictly for personal, educational, and backup purposes**. 

Downloading copyrighted content from YouTube may violate YouTube's [Terms of Service](https://www.youtube.com/t/terms) and could violate copyright laws in your jurisdiction. Under most copyright systems, private copying is only permitted for media that you legally own or for which you have obtained express licensing/permission (e.g., Creative Commons, public domain, or your own original uploads).

The developers and contributors of this software:
- Do not endorse, encourage, or facilitate copyright infringement.
- Disclaim all responsibility for any unauthorized downloading, reproduction, distribution, or misuse of media acquired through this application.
- Provide this code "as is" without warranty of any kind.

### 📄 License
This project is licensed under the **MIT License**. You are free to modify, distribute, and use the code, provided that the original copyright notice and permission notice are included in all copies. See the [LICENSE](LICENSE) file for the full text.
