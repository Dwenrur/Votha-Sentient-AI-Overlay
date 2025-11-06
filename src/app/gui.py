# src/app/gui.py
import tkinter as tk
from tkinter import scrolledtext

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
