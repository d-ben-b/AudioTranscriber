# AudioTranscriber

A small desktop tool that turns speech into text using [OpenAI Whisper](https://github.com/openai/whisper), wrapped in a minimal Tkinter GUI.

Pick one of three sources — an existing audio file, a live microphone recording, or a URL to download from — and the app transcribes it and writes the result into `transcripts/`.

## Features

- **Use an existing audio file** — browse for `.m4a`, `.mp3`, `.wav`, or anything ffmpeg can read.
- **Record audio** — captures 5 seconds of 16 kHz mono audio from the default input device.
- **Download audio** — paste a video/audio URL; `yt-dlp` fetches the best audio stream and converts it to MP3.
- Runs Whisper's `medium` model, automatically on **CUDA** when a GPU is available and on CPU otherwise.
- Transcription runs on a background thread, so the window stays responsive and shows live status.
- The loaded model is cached, so a second transcription in the same session skips the model-load cost.

## Requirements

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/) on your `PATH` (required by both Whisper and yt-dlp)
- Tkinter (bundled with most CPython installs on Windows/macOS)

## Installation

```bash
git clone https://github.com/d-ben-b/AudioTranscriber.git
cd AudioTranscriber

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
```

For **NVIDIA GPU** acceleration, install PyTorch from the CUDA index *first*, then the rest:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

CPU-only is just:

```bash
pip install -r requirements.txt
```

> **Note:** the dependency is `openai-whisper`, **not** the unrelated `whisper` package on PyPI. Installing the latter produces
> `TypeError: argument of type 'NoneType' is not iterable` on import.

On Windows, if `pip install PyAudio` fails to build, grab a prebuilt wheel: `pip install pipwin && pipwin install pyaudio`.

## Usage

```bash
python -m audio_transcriber
```

Then in the window:

1. Choose a mode:
   - **Use Existing Audio File** — click *Browse* and pick a file.
   - **Record Audio** — nothing to enter; recording starts when you press *Start*.
   - **Download Audio** — type or paste a URL into the entry field.
2. Press **Start**.
3. The status line reports progress. A dialog announces the saved transcript path when it finishes.

Installing the package also provides a console script:

```bash
pip install .
audio-transcriber
```

### Using it as a library

```python
from audio_transcriber import transcribe

text = transcribe("examples/sample.m4a", model_name="tiny")
```

## Project layout

```
audio_transcriber/
├── __init__.py       # lazy re-exports of the public helpers
├── __main__.py       # enables `python -m audio_transcriber`
├── gui.py            # Tkinter window, mode handling, output naming
├── recorder.py       # microphone capture -> WAV
├── downloader.py     # yt-dlp wrapper -> MP3
└── transcriber.py    # device selection, cached model loading, transcription
examples/
├── sample.m4a                    # short Mandarin clip to test with
└── STT_2025-12-15_13-55-19.txt   # example of a generated transcript
```

Generated files are git-ignored: downloaded and recorded audio goes to `audio/`, transcripts to `transcripts/`.

## Output

Transcripts are UTF-8 text files in `transcripts/`, named:

- `STT_<video title>.txt` for downloads (title sanitised for the filesystem)
- `STT_<YYYY-MM-DD_HH-MM-SS>.txt` for files and recordings

See [`examples/STT_2025-12-15_13-55-19.txt`](examples/STT_2025-12-15_13-55-19.txt) for a sample.

## Notes and limitations

- Recording length is fixed at 5 seconds (`RECORD_SECONDS` in `audio_transcriber/gui.py`).
- The `medium` model is ~1.5 GB, downloaded to the Whisper cache on first run, and wants roughly 5 GB of VRAM. On a smaller GPU, drop `DEFAULT_MODEL` in `transcriber.py` to `small` or `base`.
- Each download overwrites `audio/downloaded_audio.mp3`.
- Only download content you have the right to use.

## License

MIT
