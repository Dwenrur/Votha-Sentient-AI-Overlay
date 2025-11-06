# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# 🧠 Votha Sentient Overlay
> A self-hosted, sentient-style AI overlay for Twitch and OBS — your stream’s thinking companion.

---

### 🌐 Overview
**Votha Sentient Overlay** is a locally hosted, privacy-first AI companion built for streamers, creators, and tinkerers.  
It brings real-time intelligence to your Twitch streams and OBS scenes — allowing an on-screen AI to **speak, react, and adapt** to your chat and gameplay.

Unlike cloud-based AI tools, **Votha runs entirely on your machine**, giving you full control over performance, customization, and data privacy.

---

### ⚙️ Key Features

- 🎥 **OBS Integration** — Overlay system for real-time AI visuals and speech output.  
- 💬 **Twitch Chat Integration** — Reads messages, reacts dynamically, and supports event-based triggers.  
- 🧠 **Local AI Runtime** — Runs on your hardware (CPU/GPU); no external APIs required.  
- 🔊 **Voice Synthesis** — Optional text-to-speech layer that gives your AI a personality.  
- 🧩 **Modular Design** — Extend functionality through plugins or custom Python modules.  
- 🔒 **Privacy-Centric** — No data collection or telemetry — everything stays on your system.

---

### 🚀 Quickstart

**Requirements**
- Python 3.10 or higher  
- OBS Studio (with WebSocket support enabled)  
- Twitch Developer account and bot credentials  
- Basic understanding of virtual audio or TTS routing (optional)

**Installation**
```bash
git clone https://github.com/Dwenrur/Votha-Sentient-AI-Overlay.git
cd Votha-Sentient-AI-Overlay
pip install -r requirements.txt
```
or

Install using the exe when avaliable

Run
```bash
python votha.py
```

Once running, Votha will connect to your Twitch chat and OBS instance (if configured) and begin responding in real time.
You can customize AI behavior, TTS voices, and overlays through configuration files or plugin scripts.

🧾 License

This project is licensed under the PolyForm Noncommercial License 1.0.0.
You may use, modify, and distribute this project for noncommercial purposes only.
For commercial licensing, contact dwenrur@gmail.com
.

Full license: polyformproject.org/licenses/noncommercial/1.0.0

🤝 Contributing

Before contributing:

-Read CONTRIBUTING.md

-Review and sign the Contributor License Agreement (CLA)

All changes must be submitted via pull request to the protected main branch.
We require at least one review and all CI checks to pass before merging.

🧩 Future Roadmap

-Interactive emotion and expression system for overlay visuals

-Dynamic personality memory

-Multi-platform streaming support

-AI-driven moderation and community interactions

💬 Community

If you’d like to share ideas, improvements, or AI personalities — open a discussion or feature request on GitHub Issues.

“Sentience may be simulated, but creativity is real.”
— Elijah Purvey