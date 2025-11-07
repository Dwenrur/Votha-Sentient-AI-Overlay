# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# --- tiny, robust bootstrap ---
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# --- end bootstrap ---


# src/app/votha.py

import tkinter as tk
import sys
from pathlib import Path
from src.core.piper_speech import PiperSpeaker
from src.core.piper_speech import SentenceBuffer
from src.ai.llama_local import stream_from_ollama
from src.integrations.twitch_points import start_twitch_listener, redeem_queue
from src.app.gui import VothaGUI

# --- Self-locating import bootstrap (place at the very top of votha.py) ---

# votha.py lives at: <project_root>/src/app/votha.py
# We want <project_root> on sys.path so that "import src.*" works even when
# running this file directly (not as a module).
_this_file = Path(__file__).resolve()
_src_dir = _this_file.parents[1]       # .../src
_project_root = _src_dir.parent        # project root

# Insert project root at the *front* so it wins over site-packages if needed.
project_root_str = str(_project_root)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

# Optional: sanity check (no-op if everything is fine)
try:
    import src  # noqa: F401
except Exception as e:
    # As a last resort, also add the src/ directory itself.
    src_str = str(_src_dir)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
    # Re-try import; if this fails, let it raise to surface the real issue.
    import src  # noqa: F401
# --- End bootstrap ---



def main():
    # start twitch listener in background
    start_twitch_listener()

    # setup GUI
    root = tk.Tk()
    gui = VothaGUI(root)

    speaker = PiperSpeaker()
    buf = SentenceBuffer(speaker)

    def poll_redeems():
        """
        Check if Twitch sent us a channel point redeem.
        If yes: run it through Llama and speak it.
        """
        try:
            username, user_text = redeem_queue.get_nowait()
        except Exception:
            # nothing yet
            pass
        else:
            gui.add_log(f"{username}: {user_text}")
            gui.set_status("Redeem received – generating...")
            # 1) get answer from local LLM
            answer_chunks = []
            for chunk in stream_from_ollama(user_text):
                answer_chunks.append(chunk)
                buf.feed(chunk)  # will speak full sentences
            full_answer = "".join(answer_chunks)
            gui.add_log(f"Votha: {full_answer}")
            gui.set_status("Waiting for Twitch redeems...")

        # schedule next poll
        root.after(200, poll_redeems)

    # start polling
    root.after(200, poll_redeems)
    root.mainloop()

if __name__ == "__main__":
    main()
