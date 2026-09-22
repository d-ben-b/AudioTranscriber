from setuptools import find_packages, setup

setup(
    name="AudioTranscriber",
    version="1.1.0",
    description="A simple audio transcriber that uses Whisper and tkinter for UI",
    author="d-ben-b",
    url="https://github.com/d-ben-b/AudioTranscriber",
    packages=find_packages(include=["audio_transcriber", "audio_transcriber.*"]),
    install_requires=[
        "openai-whisper>=20231117",
        "torch>=2.0",
        "PyAudio>=0.2.14",
        "yt-dlp>=2024.1.1",
    ],
    entry_points={
        "console_scripts": [
            "audio-transcriber=audio_transcriber.gui:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
