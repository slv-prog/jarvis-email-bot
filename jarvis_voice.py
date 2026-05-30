import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
from faster_whisper import WhisperModel

# Load model once (downloads first time, cached after)
print("Loading Whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper ready.")

SAMPLE_RATE = 16000
DURATION = 5

def record_audio():
    """Record audio from microphone."""
    print("Recording... speak now!")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    print("Recording done.")
    return audio

def save_audio(audio):
    """Save audio to temp file."""
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(tmp.name, audio, SAMPLE_RATE)
    return tmp.name

def transcribe(filepath):
    """Transcribe audio using local Whisper model."""
    segments, _ = model.transcribe(filepath, language="en")
    text = " ".join([s.text for s in segments]).strip()
    return text

def listen_and_transcribe():
    """Full pipeline: record -> save -> transcribe -> return text."""
    audio = record_audio()
    filepath = save_audio(audio)
    try:
        text = transcribe(filepath)
        return text
    finally:
        os.unlink(filepath)