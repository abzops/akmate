import os
import uuid
import tempfile
import shutil
import re
import sys

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Flask dynamically for PyInstaller compatibility
if getattr(sys, 'frozen', False):
    template_folder = get_resource_path('templates')
    static_folder = get_resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

CORS(app)

# Helper to find ffmpeg binary
def get_ffmpeg_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    if os.path.exists("ffmpeg.exe"):
        return os.path.abspath(".")
    return None

# Temporary download directory
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "ytmp3_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# YouTube Cookies setup to bypass bot protection
COOKIES_FILE = None
if os.path.exists("cookies.txt"):
    COOKIES_FILE = "cookies.txt"
elif os.environ.get("YOUTUBE_COOKIES"):
    # Write environment variable cookies to a temp file
    temp_cookies_path = os.path.join(tempfile.gettempdir(), "youtube_cookies.txt")
    with open(temp_cookies_path, "w", encoding="utf-8") as f:
        f.write(os.environ.get("YOUTUBE_COOKIES"))
    COOKIES_FILE = temp_cookies_path



def sanitize_filename(name: str) -> str:
    """Remove characters that are unsafe for filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


@app.route("/")
def index():
    """Serve the web UI."""
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def video_info():
    """Return metadata for a YouTube video (title, thumbnail, duration)."""
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data["url"].strip()
    if not url:
        return jsonify({"error": "URL cannot be empty"}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
        "check_formats": False,
    }
    if COOKIES_FILE:
        ydl_opts["cookiefile"] = COOKIES_FILE
    
    ffmpeg_dir = get_ffmpeg_dir()
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir



    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        duration_secs = info.get("duration", 0) or 0
        minutes, seconds = divmod(int(duration_secs), 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = f"{minutes}:{seconds:02d}"

        return jsonify({
            "title": info.get("title", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "duration": duration_str,
            "duration_seconds": duration_secs,
            "channel": info.get("channel", info.get("uploader", "Unknown")),
            "view_count": info.get("view_count", 0),
        })

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Could not retrieve video info: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/api/download", methods=["GET"])
def download_audio():
    """Download YouTube audio as 320kbps MP3 and stream it to the client."""
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    # Create a unique subdirectory for this download
    job_id = uuid.uuid4().hex
    job_dir = os.path.join(DOWNLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "writethumbnail": True,
        "outtmpl": os.path.join(job_dir, "audio.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "concurrent_fragment_downloads": 8,  # 8 threads for faster downloads
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
        "check_formats": False,
    }
    if COOKIES_FILE:
        ydl_opts["cookiefile"] = COOKIES_FILE
    
    ffmpeg_dir = get_ffmpeg_dir()
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir



    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = sanitize_filename(info.get("title", "download"))

        # Find the resulting .mp3 file
        mp3_file = None
        for f in os.listdir(job_dir):
            if f.endswith(".mp3"):
                mp3_file = os.path.join(job_dir, f)
                break

        if not mp3_file or not os.path.exists(mp3_file):
            return jsonify({"error": "Conversion failed — MP3 file not found"}), 500

        download_name = f"{title}.mp3"

        def cleanup_after_send(response):
            """Remove temporary files after the response is sent."""
            try:
                shutil.rmtree(job_dir, ignore_errors=True)
            except Exception:
                pass
            return response

        response = send_file(
            mp3_file,
            as_attachment=True,
            download_name=download_name,
            mimetype="audio/mpeg",
        )
        response.call_on_close(lambda: shutil.rmtree(job_dir, ignore_errors=True))
        return response

    except yt_dlp.utils.DownloadError as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        return jsonify({"error": f"Download failed: {str(e)}"}), 400
    except Exception as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    import threading
    port = int(os.environ.get("PORT", 5000))
    is_frozen = getattr(sys, 'frozen', False)
    
    def start_flask():
        app.run(host="127.0.0.1", port=port, debug=False)

    if is_frozen or os.environ.get("DESKTOP_MODE") == "true":
        # Launch in native desktop app window (pywebview)
        try:
            import webview
            
            # Run Flask server in a background thread
            server_thread = threading.Thread(target=start_flask)
            server_thread.daemon = True
            server_thread.start()
            
            # Start GUI window
            webview.create_window(
                title="YT MP3 Downloader",
                url=f"http://127.0.0.1:{port}",
                width=800,
                height=700,
                resizable=True,
                min_size=(640, 500)
            )
            webview.start()
            sys.exit(0)
        except Exception as e:
            print(f"Failed to start desktop mode: {e}. Falling back to browser...")

    # Default browser fallback mode
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open(f"http://127.0.0.1:{port}")

    if is_frozen or os.environ.get("AUTO_OPEN") != "false":
        Timer(1.5, open_browser).start()
    
    app.run(host="127.0.0.1", port=port, debug=not is_frozen)
