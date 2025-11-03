import os
import json
import time
import asyncio
import threading
import requests
import websockets

from piper_speech import PiperSpeaker, SentenceBuffer

# ---------- LLM (Ollama, llama3.1:8b) ----------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1:8b"

def stream_from_ollama(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    with requests.post(OLLAMA_URL, json=payload, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            msg = data.get("message", {})
            content = msg.get("content", "")
            if content:
                yield content
            if data.get("done"):
                break

# ---------- overlay websocket (ws://localhost:8765) ----------
WS_PORT = 8765
_connected = set()
_loop = None  # event loop for ws thread

async def _ws_handler(ws):
    _connected.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        _connected.remove(ws)

async def _ws_server():
    async with websockets.serve(_ws_handler, "localhost", WS_PORT):
        print(f"[overlay] WebSocket server running on ws://localhost:{WS_PORT}")
        await asyncio.Future()  # run forever

def start_ws_thread():
    global _loop
    _loop = asyncio.new_event_loop()
    def _run():
        asyncio.set_event_loop(_loop)
        _loop.run_until_complete(_ws_server())
    t = threading.Thread(target=_run, daemon=True)
    t.start()

def send_overlay(state: str, text: str = ""):
    """thread-safe send to all overlay clients"""
    if _loop is None or not _connected:
        return
    async def _broadcast():
        msg = json.dumps({"state": state, "text": text})
        await asyncio.gather(*(ws.send(msg) for ws in list(_connected)))
    asyncio.run_coroutine_threadsafe(_broadcast(), _loop)

# ---------- main ----------
def main():
    print(f"Starting Votha with local {MODEL_NAME} + Piper + overlay...\n")

    # 1) start websocket server in background
    start_ws_thread()

    # 2) start voice
    speaker = PiperSpeaker()
    buf = SentenceBuffer(speaker)

    while True:
        user = input("You: ")
        if user.lower() in ("quit", "exit", "stop"):
            break

        print("Votha:", end=" ", flush=True)

        # tell overlay we're thinking / reflective
        send_overlay("reflective", user)

        sentence_buf = ""

        for chunk in stream_from_ollama(user):
            print(chunk, end="", flush=True)
            sentence_buf += chunk
            # feed to TTS buffer
            buf.feed(chunk)
            # also send partial text to overlay if you want:
            # send_overlay("speaking", sentence_buf)

        print()
        # when done, go idle
        send_overlay("idle", "")

    speaker.close()

if __name__ == "__main__":
    # make sure Ollama is running!
    main()
