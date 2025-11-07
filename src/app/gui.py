# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/
# src/app/gui.py
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from src.app.settings_tab import SettingsTab

class VothaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Votha – Sentient Overlay")

        self.status_var = tk.StringVar(value="Waiting for Twitch redeems...")
        tk.Label(root, textvariable=self.status_var).pack(anchor="w", padx=8, pady=4)

        self.log = scrolledtext.ScrolledText(root, height=10, width=60)
        self.log.pack(padx=8, pady=4)

    def set_status(self, text: str):
        self.status_var.set(text)

    def add_log(self, text: str):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Votha")

        # if you already have a Notebook, reuse it.
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # ... your existing tabs ...
        # self.notebook.add(existing_frame, text="Home")

        # NEW: Settings tab
        self.settings_tab = SettingsTab(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")