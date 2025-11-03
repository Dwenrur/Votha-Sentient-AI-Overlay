import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPER = os.path.join(BASE_DIR, "piper", "piper.exe")
MODEL = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx")
CFG   = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx.json")

out_wav = os.path.join(BASE_DIR, "test_out.wav")

cmd = [
    PIPER,
    "-m", MODEL,
    "-c", CFG,
    "-f", out_wav,
]

print("Running:", " ".join(cmd))

proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
)
proc.communicate(input=b"Hello, this is a direct Piper test.\n")

print("Done. WAV exists:", os.path.exists(out_wav), "size:", os.path.getsize(out_wav) if os.path.exists(out_wav) else 0)
