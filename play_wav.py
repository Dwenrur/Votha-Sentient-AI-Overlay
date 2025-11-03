import os
import simpleaudio as sa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
wav_path = os.path.join(BASE_DIR, "test_out.wav")

print("Trying to play:", wav_path)

if not os.path.exists(wav_path):
    raise FileNotFoundError("test_out.wav not found. Run make_wav.py first.")

wave_obj = sa.WaveObject.from_wave_file(wav_path)
play_obj = wave_obj.play()
play_obj.wait_done()
print("Played.")
