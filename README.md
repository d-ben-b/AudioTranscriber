# AudioTranscriber

A small desktop tool that turns speech into text using [OpenAI Whisper](https://github.com/openai/whisper), wrapped in a minimal Tkinter GUI.

Pick one of three sources — an existing audio file, a live microphone recording, or a URL to download from — and the app transcribes it and writes the result to a `.txt` file next to the script.

## Features

- **Use an existing audio file** — browse for `.m4a`, `.wav`, or any format ffmpeg can read.
- **Record audio** — captures 5 seconds of 16 kHz mono audio from the default input device into `recorded_audio.wav`.
- **Download audio** — paste a video/audio URL; `yt-dlp` fetches the best audio stream and converts it to `downloaded_audio.mp3`.
- Runs Whisper's `medium` model, automatically on **CUDA** when a GPU is available and on CPU otherwise.
- Transcription runs on a background thread so the window stays responsive.
- Output is saved as `STT_<video title>.txt` for downloads, or `STT_<YYYY-MM-DD_HH-MM-SS>.txt` otherwise.

## Requirements

- Python 3.6+
- [ffmpeg](https://ffmpeg.org/) available on `PATH` (required by both Whisper and yt-dlp)
- Tkinter (bundled with most CPython installs on Windows/macOS)

Python packages:

```
openai-whisper
torch
pyaudio
yt-dlp
```

## Installation

```bash
git clone https://github.com/d-ben-b/AudioTranscriber.git
cd AudioTranscriber

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install openai-whisper torch pyaudio yt-dlp
```

On Windows, if `pip install pyaudio` fails to build, install a prebuilt wheel instead:

```bash
pip install pipwin && pipwin install pyaudio
```

For GPU acceleration, install the CUDA build of PyTorch from [pytorch.org](https://pytorch.org/get-started/locally/) rather than the default CPU wheel.

## Usage

```bash
python stt_transcriber.py
```

Then in the window:

1. Choose a mode:
   - **Use Existing Audio File** — click *Browse* and pick a file.
   - **Record Audio** — nothing to enter; recording starts when you press *Start*.
   - **Download Audio** — type or paste a URL into the entry field.
2. Press **Start**.
3. Wait for the model to load and transcribe. A dialog reports the name of the saved transcript.

The project is also installable as a console script:

```bash
pip install .
audio-transcriber
```

## Project layout

| File | Purpose |
| --- | --- |
| `stt_transcriber.py` | Tkinter GUI, microphone recording, and Whisper transcription |
| `downLoad.py` | `download_audio(url)` — yt-dlp wrapper that saves audio as MP3 |
| `setup.py` | Packaging metadata and the `audio-transcriber` entry point |
| `constraints.txt` | Pinned versions from the development environment |

## Notes and limitations

- Recording length is fixed at 5 seconds (`record_seconds=5` in `process_audio`); change it in the source to record longer.
- The `medium` model is roughly 1.5 GB and is downloaded to the Whisper cache on first run.
- Downloaded audio always lands at `downloaded_audio.mp3`, so each download overwrites the previous one.
- Only download content you have the right to use.

## License

MIT
