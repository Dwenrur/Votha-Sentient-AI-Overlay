from pathlib import Path
import os
import subprocess
import tempfile
import sounddevice as sd
import soundfile as sf
from src.utils.config import load_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]
cfg = load_config()

PIPER_PATH  = PROJECT_ROOT / cfg["tts"].get("piper_path", "piper/piper.exe")
MODEL_PATH  = PROJECT_ROOT / cfg["tts"].get("voice_model", "piper/voices/en_US-norman-medium.onnx")
CONFIG_PATH = PROJECT_ROOT / cfg["tts"].get("voice_config","piper/voices/en_US-norman-medium.onnx.json")

AUDIO_DEVICE = cfg.get("audio", {}).get("device")


cfg = load_config()
AUDIO_DEVICE = cfg.get("audio", {}).get("device")  # e.g., 22

def synth_and_play(text: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    proc = subprocess.Popen(
        [
            str(PIPER_PATH),
            "-m", str(MODEL_PATH),
            "-c", str(CONFIG_PATH),
            "-f", wav_path,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc.communicate(input=(text.strip() + "\n").encode("utf-8"))

    data, samplerate = sf.read(wav_path, dtype="float32")
    try:
        if AUDIO_DEVICE is not None:
            sd.play(data, samplerate, device=AUDIO_DEVICE)
        else:
            sd.play(data, samplerate)
        sd.wait()
    finally:
        try:
            os.remove(wav_path)
        except OSError:
            pass

class PiperSpeaker:
    def speak(self, text: str):
        synth_and_play(text)
    def close(self):
        pass

class SentenceBuffer:
    ENDERS = (".", "?", "!", "\n")
    def __init__(self, speaker: PiperSpeaker):
        self.speaker = speaker
        self._buf = ""
    def feed(self, chunk: str, force: bool = False):
        self._buf += chunk
        if force or any(self._buf.endswith(e) for e in self.ENDERS):
            sent = self._buf.strip()
            if sent:
                self.speaker.speak(sent)
            self._buf = ""
