"""Audio download via yt-dlp."""

from pathlib import Path

import yt_dlp

DEFAULT_STEM = "downloaded_audio"


class DownloadError(RuntimeError):
    """Raised when yt-dlp could not fetch the requested audio."""


def download_audio(url, output_dir=".", stem=DEFAULT_STEM):
    """Download the best audio stream for `url` and convert it to MP3.

    Returns a `(path, title)` tuple. Raises `DownloadError` on failure.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": str(output_dir / f"{stem}.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",  # 數值越高音質越高
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as exc:  # yt-dlp raises a wide range of network errors
        raise DownloadError(f"下載失敗: {exc}") from exc

    title = info.get("title") or stem
    path = output_dir / f"{stem}.mp3"
    if not path.exists():
        raise DownloadError(f"下載完成但找不到輸出檔案: {path}")

    print(f"音訊 '{title}' 已成功下載並轉換為 MP3 格式！")
    return path, title
