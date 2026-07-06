# 🎵 YT MP3 — YouTube to 320kbps MP3 Downloader

A beautiful web application that converts YouTube videos to high-quality **320kbps MP3** audio files.

Built with **Flask**, **yt-dlp**, and **FFmpeg**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🎵 **320kbps MP3** — Maximum quality audio extraction
- 📋 **Paste & Go** — One-click clipboard paste
- 🖼️ **Video Preview** — Title, thumbnail, channel, duration, and view count
- 📱 **Responsive** — Works on desktop and mobile
- 🎨 **Premium UI** — Dark theme with glassmorphism and animations
- ⚡ **Fast** — Streams the file directly to your browser
- 🏷️ **Metadata** — Embeds thumbnail and metadata into the MP3

---

## 🚀 Quick Start (Local)

### Prerequisites

- **Python 3.9+**
- **FFmpeg** — Required for audio conversion

**Install FFmpeg:**

```bash
# Windows (via Chocolatey)
choco install ffmpeg

# Windows (via Scoop)
scoop install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-mp3-downloader.git
cd youtube-mp3-downloader

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open **http://localhost:5000** in your browser. 🎉

---

## 🌐 Deploy to Render (Free)

### One-Click Deploy

1. **Push this code to a GitHub repository**
2. Go to [render.com](https://render.com) and sign up (free)
3. Click **New → Web Service**
4. Connect your GitHub repo
5. Render auto-detects the `render.yaml` and `Dockerfile`
6. Click **Create Web Service**

That's it! Your app will be live at `https://your-app-name.onrender.com`.

> **Note:** The free tier spins down after 15 minutes of inactivity. The first request after idle takes ~30 seconds to wake up.

### Manual Deploy

If you prefer manual setup on Render:

| Setting            | Value                                        |
|--------------------|----------------------------------------------|
| **Runtime**        | Docker                                       |
| **Dockerfile Path**| `./Dockerfile`                               |
| **Plan**           | Free                                         |
| **Health Check**   | `/`                                          |

---

## 📡 API Reference

### `POST /api/info`

Get video metadata.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "title": "Rick Astley - Never Gonna Give You Up",
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "duration": "3:33",
  "duration_seconds": 213,
  "channel": "Rick Astley",
  "view_count": 1500000000
}
```

### `GET /api/download?url=<youtube_url>`

Download the audio as a 320kbps MP3 file.

**Response:** Binary MP3 file stream with `Content-Disposition: attachment` header.

---

## 🛠️ Tech Stack

| Component   | Technology           |
|-------------|----------------------|
| Backend     | Flask + Gunicorn     |
| Downloader  | yt-dlp               |
| Converter   | FFmpeg (320kbps MP3) |
| Frontend    | Vanilla HTML/CSS/JS  |
| Deployment  | Docker + Render      |

---

## ⚠️ Disclaimer

This tool is intended for **personal use only**. Downloading copyrighted content from YouTube may violate their [Terms of Service](https://www.youtube.com/t/terms). Only download content you have the right to use (e.g., your own uploads, Creative Commons licensed content).

The developers of this tool are not responsible for any misuse.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
