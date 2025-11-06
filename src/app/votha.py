# src/app/votha.py
import tkinter as tk
from src.core.piper_speech import PiperSpeaker
from src.core.piper_speech import SentenceBuffer
from src.ai.llama_local import stream_from_ollama
from src.integrations.twitch_points import start_twitch_listener, redeem_queue
from src.app.gui import VothaGUI

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
