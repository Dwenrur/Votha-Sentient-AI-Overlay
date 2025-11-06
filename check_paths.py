# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

piper = os.path.join(BASE_DIR, "piper", "piper.exe")
model = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx")
cfg   = os.path.join(BASE_DIR, "piper", "voices", "en_US-norman-medium.onnx.json")

print("PIPER:", piper, os.path.exists(piper))
print("MODEL:", model, os.path.exists(model))
print("CFG  :", cfg,   os.path.exists(cfg))
