# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# src/app/settings_tab.py
import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# --- CONFIG LOCATIONS ---
CONFIG_DIR_USER = Path.home() / ".votha"
CONFIG_PATH_USER = CONFIG_DIR_USER / "config.json"

# project-local (repo) path, autodetect relative to current file
CONFIG_PATH_PROJECT = Path(__file__).resolve().parents[2] / "config" / "votha-config.json"

TWITCH_KEYS = [
    "twitch.client_id",
    "twitch.client_secret",
    "twitch.broadcaster_id",
    "twitch.reward_id",
    "twitch.user_access_token",
]

# --- helpers ---

def _find_existing_config() -> Path | None:
    """Return whichever config file exists first (project-local beats user)."""
    if CONFIG_PATH_PROJECT.exists():
        return CONFIG_PATH_PROJECT
    if CONFIG_PATH_USER.exists():
        return CONFIG_PATH_USER
    return None

def _load_existing() -> dict:
    for path in (CONFIG_PATH_PROJECT, CONFIG_PATH_USER):
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {}

def _ensure_config_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def _deep_set(d: dict, dotted_key: str, value: str):
    parts = dotted_key.split(".")
    cur = d
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value

def _deep_get(d: dict, dotted_key: str, default: str = "") -> str:
    parts = dotted_key.split(".")
    cur = d
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur if isinstance(cur, str) else default

# --- main widget ---

class SettingsTab(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.vars = {key: tk.StringVar() for key in TWITCH_KEYS}

        # Load whichever config exists (project or user)
        cfg = _load_existing()
        for k, v in self.vars.items():
            v.set(_deep_get(cfg, k, os.environ.get(k.upper().replace(".", "_"), "")))

        # GUI layout
        row = 0
        self._add_entry("Client ID", "twitch.client_id", row); row += 1
        self._add_entry("Client Secret", "twitch.client_secret", row, show="•"); row += 1
        self._add_entry("Broadcaster ID", "twitch.broadcaster_id", row); row += 1
        self._add_entry("Reward ID (optional)", "twitch.reward_id", row); row += 1
        self._add_entry("User Access Token", "twitch.user_access_token", row, show="•"); row += 1

        buttons = ttk.Frame(self)
        buttons.grid(row=row, column=0, columnspan=2, pady=(12, 0), sticky="ew")
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        ttk.Button(buttons, text="Save", command=self._on_save).grid(row=0, column=0, padx=4, sticky="ew")
        ttk.Button(buttons, text="Test Connection", command=self._on_test).grid(row=0, column=1, padx=4, sticky="ew")

        note = ttk.Label(
            self,
            text="Scopes required: channel:read:redemptions (user token).",
            foreground="#666"
        )
        note.grid(row=row+1, column=0, columnspan=2, pady=(8, 0), sticky="w")

    def _add_entry(self, label, key, row, show=""):
        ttk.Label(self, text=label).grid(row=row, column=0, padx=(6, 8), pady=6, sticky="e")
        entry = ttk.Entry(self, textvariable=self.vars[key], show=show, width=44)
        entry.grid(row=row, column=1, padx=(0, 6), pady=6, sticky="w")

    def _on_save(self):
        # Load whichever config we have (project-local wins)
        existing_path = _find_existing_config() or CONFIG_PATH_USER
        cfg = _load_existing()

        for k, var in self.vars.items():
            _deep_set(cfg, k, var.get().strip())

        try:
            _ensure_config_dir(existing_path)
            with open(existing_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save config:\n{e}")
            return

        # Reflect into environment
        for k, var in self.vars.items():
            os.environ[k.upper().replace(".", "_")] = var.get().strip()

        messagebox.showinfo("Saved", f"Settings saved to {existing_path}")

    def _on_test(self):
        """Verify your Twitch credentials via Helix."""
        cid = self.vars["twitch.client_id"].get().strip()
        token = self.vars["twitch.user_access_token"].get().strip()
        bid = self.vars["twitch.broadcaster_id"].get().strip()

        if not (cid and token and bid):
            messagebox.showwarning("Missing", "Client ID, User Token, and Broadcaster ID required.")
            return

        headers = {"Client-Id": cid, "Authorization": f"Bearer {token}"}
        try:
            r = requests.get("https://api.twitch.tv/helix/users", headers=headers, timeout=10)
            if r.status_code == 401:
                messagebox.showerror("Unauthorized", "Bad token or missing scope channel:read:redemptions.")
                return
            r.raise_for_status()
            user = (r.json().get("data") or [{}])[0]
            name = user.get("login") or "unknown"

            r2 = requests.get(f"https://api.twitch.tv/helix/users?id={bid}", headers=headers, timeout=10)
            r2.raise_for_status()
            found = bool(r2.json().get("data"))
            if not found:
                messagebox.showerror("Not Found", f"Broadcaster ID {bid} not found.")
                return

            messagebox.showinfo("Success", f"Token OK (logged in as @{name}), broadcaster {bid} found.")
        except requests.RequestException as e:
            messagebox.showerror("Network Error", str(e))
