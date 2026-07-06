/**
 * YT MP3 Downloader — Frontend Logic
 * Handles URL input, video info fetching, and MP3 download.
 */

(function () {
    "use strict";

    // === DOM Elements ===
    const urlInput     = document.getElementById("urlInput");
    const pasteBtn     = document.getElementById("pasteBtn");
    const fetchBtn     = document.getElementById("fetchBtn");
    const errorBox     = document.getElementById("errorBox");
    const errorText    = document.getElementById("errorText");
    const infoCard     = document.getElementById("infoCard");
    const thumbnail    = document.getElementById("thumbnail");
    const duration     = document.getElementById("duration");
    const videoTitle   = document.getElementById("videoTitle");
    const channelName  = document.getElementById("channelName");
    const viewsEl      = document.getElementById("views");
    const downloadBtn  = document.getElementById("downloadBtn");
    const progressSection = document.getElementById("progressSection");
    const progressFill = document.getElementById("progressFill");
    const progressText = document.getElementById("progressText");

    let currentUrl = "";

    // === Utility: Show / Hide ===
    function showError(msg) {
        errorText.textContent = msg;
        errorBox.classList.remove("hidden");
        // Auto-hide after 8 seconds
        setTimeout(() => errorBox.classList.add("hidden"), 8000);
    }

    function hideError() {
        errorBox.classList.add("hidden");
    }

    function setLoading(btn, loading) {
        if (loading) {
            btn.classList.add("loading");
        } else {
            btn.classList.remove("loading");
        }
    }

    function formatViews(count) {
        if (!count) return "N/A";
        if (count >= 1_000_000_000) return (count / 1_000_000_000).toFixed(1) + "B views";
        if (count >= 1_000_000) return (count / 1_000_000).toFixed(1) + "M views";
        if (count >= 1_000) return (count / 1_000).toFixed(1) + "K views";
        return count.toLocaleString() + " views";
    }

    function isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|shorts\/|embed\/|v\/)|youtu\.be\/|music\.youtube\.com\/watch\?v=)/;
        return pattern.test(url);
    }

    // === Paste from clipboard ===
    pasteBtn.addEventListener("click", async () => {
        try {
            const text = await navigator.clipboard.readText();
            urlInput.value = text;
            urlInput.focus();
            // Add a quick flash animation
            urlInput.style.borderColor = "var(--accent-primary)";
            setTimeout(() => urlInput.style.borderColor = "", 500);
        } catch (err) {
            showError("Could not read clipboard. Please paste manually.");
        }
    });

    // === Fetch video info ===
    fetchBtn.addEventListener("click", fetchVideoInfo);
    urlInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") fetchVideoInfo();
    });

    async function fetchVideoInfo() {
        hideError();
        const url = urlInput.value.trim();

        if (!url) {
            showError("Please enter a YouTube URL.");
            urlInput.focus();
            return;
        }

        if (!isValidYouTubeUrl(url)) {
            showError("That doesn't look like a valid YouTube URL. Please check and try again.");
            return;
        }

        setLoading(fetchBtn, true);
        infoCard.classList.add("hidden");

        try {
            const resp = await fetch("/api/info", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });

            const data = await resp.json();

            if (!resp.ok) {
                throw new Error(data.error || "Failed to fetch video info.");
            }

            // Populate info card
            thumbnail.src = data.thumbnail;
            thumbnail.alt = data.title;
            duration.textContent = data.duration;
            videoTitle.textContent = data.title;
            channelName.textContent = data.channel;
            viewsEl.textContent = formatViews(data.view_count);

            currentUrl = url;
            infoCard.classList.remove("hidden");

            // Reset download state
            progressSection.classList.add("hidden");
            downloadBtn.classList.remove("loading");

        } catch (err) {
            showError(err.message);
        } finally {
            setLoading(fetchBtn, false);
        }
    }

    // === Download MP3 ===
    downloadBtn.addEventListener("click", downloadMP3);

    async function downloadMP3() {
        if (!currentUrl) {
            showError("No video selected. Fetch video info first.");
            return;
        }

        hideError();
        setLoading(downloadBtn, true);
        progressSection.classList.remove("hidden");
        progressFill.style.width = "0%";
        progressText.textContent = "Starting download and conversion...";

        // Simulate progress since we can't get real progress from a streaming download
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 85) {
                progress += Math.random() * 8;
                progress = Math.min(progress, 85);
                progressFill.style.width = progress + "%";

                if (progress < 30) {
                    progressText.textContent = "Downloading audio from YouTube...";
                } else if (progress < 60) {
                    progressText.textContent = "Converting to 320kbps MP3...";
                } else {
                    progressText.textContent = "Finalizing your MP3 file...";
                }
            }
        }, 600);

        try {
            const resp = await fetch(`/api/download?url=${encodeURIComponent(currentUrl)}`);

            clearInterval(progressInterval);

            if (!resp.ok) {
                let errMsg = "Download failed.";
                try {
                    const errData = await resp.json();
                    errMsg = errData.error || errMsg;
                } catch (_) { /* response may not be JSON */ }
                throw new Error(errMsg);
            }

            // Get filename from Content-Disposition header
            const disposition = resp.headers.get("Content-Disposition");
            let filename = "download.mp3";
            if (disposition) {
                const match = disposition.match(/filename\*?=(?:UTF-8'')?["']?([^"';\n]+)/i);
                if (match) filename = decodeURIComponent(match[1]);
            }

            // Convert response to blob and trigger download
            progressFill.style.width = "95%";
            progressText.textContent = "Preparing download...";

            const blob = await resp.blob();

            progressFill.style.width = "100%";
            progressText.textContent = "Download complete! ✓";

            // Trigger browser download
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(a.href);

            // Success state
            setTimeout(() => {
                progressText.textContent = "Your MP3 has been downloaded!";
            }, 500);

        } catch (err) {
            clearInterval(progressInterval);
            progressSection.classList.add("hidden");
            showError(err.message);
        } finally {
            setLoading(downloadBtn, false);
        }
    }

    // === Auto-focus input on load ===
    urlInput.focus();

})();
