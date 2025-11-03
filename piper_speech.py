import os
import subprocess
import tempfile
import simpleaudio as sa
import sounddevice as sd
import soundfile as sf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPER_PATH = os.path.join(BASE_DIR, "piper", "piper.exe")
MODEL_PATH = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx")
CONFIG_PATH = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx.json")


def synth_and_play(text: str):
    # make a temp wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    # run piper ONCE to synthesize the text
    proc = subprocess.Popen(
        [
            PIPER_PATH,
            "-m", MODEL_PATH,
            "-c", CONFIG_PATH,
            "-f", wav_path,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc.communicate(input=(text.strip() + "\n").encode("utf-8"))

    # now play it
    try:
        data, samplerate = sf.read(wav_path, dtype="float32")

        # 1) env override (so you can force it)
        env_device = os.environ.get("VOTHA_AUDIO_DEVICE", "").strip()

        target_device = None

        if env_device:
            # user said "use this id"
            try:
                target_device = int(env_device)
                print(f"[INFO] Using device index from env: {target_device}")
            except ValueError:
                # user gave a name
                target_device = env_device
                print(f"[INFO] Using device name from env: {target_device}")
        else:
            # 2) try to find VB cable by name
            devices = sd.query_devices()
            for idx, dev in enumerate(devices):
                name = dev["name"].lower()
                # your list has "VIRTUAL CABLE (VB-Audio Virtual Cable)"
                if ("virtual cable" in name) or ("vb-audio" in name) or ("cable output" in name):
                    # must be an output device
                    if dev["max_output_channels"] > 0:
                        target_device = idx
                        print(f"[INFO] Auto-selected audio device {idx}: {dev['name']}")
                        break

            # 3) if still nothing, fallback to your actual one we saw: 22
            if target_device is None:
                target_device = 22  # from your device list (WASAPI virtual cable)
                print("[WARN] Could not auto-detect VB-CABLE, falling back to device 22.")
                print("       You can override with: set VOTHA_AUDIO_DEVICE=22")

        # finally: play
        sd.play(data, samplerate, device=target_device)
        sd.wait()

    except Exception as e:
        print(f"[ERROR] Playback failed, using default output. Reason: {e}")
        # fallback to default output
        try:
            data, samplerate = sf.read(wav_path, dtype="float32")
            sd.play(data, samplerate)
            sd.wait()
        except Exception as e2:
            print(f"[ERROR] Even default playback failed: {e2}")

    # clean up
    try:
        os.remove(wav_path)
    except OSError:
        pass



class PiperSpeaker:
    def speak(self, text: str):

        # speak immediately
        synth_and_play(text)
        
    def close(self):
        pass  # nothing to close


class SentenceBuffer:
    ENDERS = (".", "?", "!", "\n")

    def __init__(self, speaker: PiperSpeaker):
        self.speaker = speaker
        self._buf = ""

    def feed(self, chunk: str):
        self._buf += chunk
        if any(self._buf.endswith(e) for e in self.ENDERS):
            sentence = self._buf.strip()
            if sentence:
                self.speaker.speak(sentence)
            self._buf = ""
