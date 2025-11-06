# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/
# src/ai/llama_local.py
import json, requests
from src.utils.config import load_config

_cfg = load_config()
_ollama_url = _cfg["llm"]["url"]
_model_name = _cfg["model"]["name"]
_opts = {
    "temperature": _cfg["model"].get("temperature", 0.7),
    "top_p": _cfg["model"].get("top_p", 0.9),
    "num_predict": _cfg["model"].get("max_tokens", 200)
}

def stream_from_ollama(prompt: str):
    url = f"{_ollama_url}/api/chat"
    payload = {
        "model": _model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "options": _opts
    }
    with requests.post(url, json=payload, stream=True) as r:
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
