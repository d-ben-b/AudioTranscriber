"""Whisper model loading and transcription."""

import functools

import torch
import whisper

DEFAULT_MODEL = "medium"


def get_device():
    """Return the device Whisper should run on."""
    return "cuda" if torch.cuda.is_available() else "cpu"


@functools.lru_cache(maxsize=2)
def load_model(model_name=DEFAULT_MODEL, device=None):
    """Load a Whisper model onto the best available device.

    Cached so that repeated transcriptions reuse the already-loaded weights
    instead of paying the multi-second load cost every time.
    """
    device = device or get_device()
    return whisper.load_model(model_name, device=device)


def transcribe(audio_path, model_name=DEFAULT_MODEL, device=None):
    """Transcribe `audio_path` and return the recognised text."""
    model = load_model(model_name, device)
    result = model.transcribe(str(audio_path))
    return result["text"]
