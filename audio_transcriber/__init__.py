"""Speech-to-text desktop tool built on OpenAI Whisper."""

__version__ = "1.1.0"

__all__ = ["download_audio", "record_audio", "transcribe"]


def __getattr__(name):
    # Imported lazily so that `import audio_transcriber` stays cheap and does
    # not pull in torch/whisper/pyaudio until something is actually used.
    if name == "download_audio":
        from audio_transcriber.downloader import download_audio

        return download_audio
    if name == "record_audio":
        from audio_transcriber.recorder import record_audio

        return record_audio
    if name == "transcribe":
        from audio_transcriber.transcriber import transcribe

        return transcribe
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
