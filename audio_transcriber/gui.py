"""Tkinter front-end for the transcriber."""

import re
import time
import tkinter as tk
from pathlib import Path
from threading import Thread
from tkinter import filedialog, messagebox

from audio_transcriber.downloader import download_audio
from audio_transcriber.recorder import record_audio
from audio_transcriber.transcriber import DEFAULT_MODEL, get_device, transcribe

MODE_FILE = 1
MODE_RECORD = 2
MODE_URL = 3

RECORD_SECONDS = 5
OUTPUT_DIR = Path("transcripts")
WORK_DIR = Path("audio")


def safe_filename(name, fallback="transcript"):
    """Strip characters that are not allowed in Windows/POSIX file names."""
    cleaned = re.sub(r'[<>:"/\|?*\x00-\x1f]', "_", name).strip(" .")
    return cleaned[:120] or fallback


class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Transcriber with Whisper")

        self.mode = tk.IntVar(value=MODE_FILE)
        self.status = tk.StringVar(value=f"Ready ({get_device()}, model: {DEFAULT_MODEL})")

        tk.Radiobutton(
            root, text="Use Existing Audio File", variable=self.mode, value=MODE_FILE
        ).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(
            root, text="Record Audio", variable=self.mode, value=MODE_RECORD
        ).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(
            root, text="Download Audio", variable=self.mode, value=MODE_URL
        ).grid(row=2, column=0, sticky=tk.W)

        self.entry_source = tk.Entry(root, width=40)
        self.entry_source.grid(row=3, column=0, padx=10, pady=10)

        tk.Button(root, text="Browse", command=self.browse_file).grid(row=3, column=1)

        self.btn_start = tk.Button(root, text="Start", command=self.start_processing)
        self.btn_start.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Label(root, textvariable=self.status, anchor=tk.W).grid(
            row=5, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=(0, 10)
        )

    # -- UI helpers ---------------------------------------------------------

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio files", "*.m4a *.mp3 *.wav *.flac *.ogg"),
                ("All files", "*.*"),
            ]
        )
        if file_path:
            self.entry_source.delete(0, tk.END)
            self.entry_source.insert(0, file_path)

    def set_status(self, text):
        # Tk is not thread-safe, so worker threads hop back to the main loop.
        self.root.after(0, self.status.set, text)

    def finish(self, kind, title, message):
        def show():
            self.btn_start.config(state=tk.NORMAL)
            self.status.set(f"Ready ({get_device()}, model: {DEFAULT_MODEL})")
            (messagebox.showinfo if kind == "info" else messagebox.showerror)(
                title, message
            )

        self.root.after(0, show)

    # -- Work ---------------------------------------------------------------

    def start_processing(self):
        self.btn_start.config(state=tk.DISABLED)
        Thread(target=self.process_audio, daemon=True).start()

    def resolve_source(self):
        """Return a `(audio_path, output_stem)` pair for the selected mode."""
        mode = self.mode.get()

        if mode == MODE_RECORD:
            WORK_DIR.mkdir(parents=True, exist_ok=True)
            self.set_status(f"Recording {RECORD_SECONDS}s...")
            path = record_audio(
                WORK_DIR / "recorded_audio.wav", record_seconds=RECORD_SECONDS
            )
            return path, time.strftime("%Y-%m-%d_%H-%M-%S")

        source = self.entry_source.get().strip()

        if mode == MODE_FILE:
            if not source:
                raise ValueError("Please provide an audio file.")
            path = Path(source)
            if not path.is_file():
                raise ValueError(f"File not found: {path}")
            return path, time.strftime("%Y-%m-%d_%H-%M-%S")

        if not source:
            raise ValueError("Please provide a URL.")
        self.set_status("Downloading audio...")
        path, title = download_audio(source, output_dir=WORK_DIR)
        return path, safe_filename(title)

    def process_audio(self):
        try:
            audio_path, stem = self.resolve_source()

            self.set_status(f"Transcribing on {get_device()}...")
            text = transcribe(audio_path)

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = OUTPUT_DIR / f"STT_{stem}.txt"
            out_path.write_text(text, encoding="utf-8")
        except Exception as exc:
            self.finish("error", "Error", str(exc))
        else:
            self.finish("info", "Success", f"Transcription saved to {out_path}")


def main():
    root = tk.Tk()
    TranscriberApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
