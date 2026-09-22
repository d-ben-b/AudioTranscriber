"""Microphone capture."""

import wave

import pyaudio

DEFAULT_SAMPLE_RATE = 16000  # Whisper resamples everything to 16 kHz anyway.
DEFAULT_CHUNK_SIZE = 1024


def record_audio(
    file_name,
    record_seconds=5,
    sample_rate=DEFAULT_SAMPLE_RATE,
    chunk_size=DEFAULT_CHUNK_SIZE,
):
    """Record mono 16-bit audio from the default input device into a WAV file.

    Returns the path that was written.
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )
    print("Recording...")
    frames = []
    try:
        for _ in range(int(sample_rate / chunk_size * record_seconds)):
            frames.append(stream.read(chunk_size))
    finally:
        stream.stop_stream()
        stream.close()
        sample_width = audio.get_sample_size(pyaudio.paInt16)
        audio.terminate()
    print("Recording finished.")

    with wave.open(str(file_name), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
    return file_name
