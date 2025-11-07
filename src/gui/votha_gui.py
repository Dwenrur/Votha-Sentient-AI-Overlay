import os
import sys
import signal
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --- Paths that match YOUR repo -------------------------------------------
# This file lives at src/gui/votha_gui.py  → repo root is two levels up.
REPO_ROOT   = Path(__file__).resolve().parents[2]        # src/gui -> src -> (repo root)
VOTHA_ENTRY = REPO_ROOT / "src" / "app" / "votha.py"     # main entry you’re using
# If you keep config in repo/config/, this is a sensible default:
DEFAULT_CONFIG = (REPO_ROOT / "config" / "votha-config.json")
PYTHON_EXE  = sys.executable
# --------------------------------------------------------------------------

CREATE_NEW_PROCESS_GROUP = 0x00000200 if os.name == "nt" else 0

class VothaController:
    def __init__(self, log_cb):
        self.proc: subprocess.Popen | None = None
        self._stop_reader = threading.Event()
        self.log_cb = log_cb
        self.env = os.environ.copy()
        # Don’t force a config path; let the user pick. If you want a default, uncomment next line:
        # self.env.setdefault("VOTHA_CONFIG", str(DEFAULT_CONFIG))
        self.env.setdefault("VOTHA_LOG_LEVEL", "INFO")

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def start(self):
        if self.is_running():
            self.log_cb("[GUI] Votha is already running.\n")
            return
        if not VOTHA_ENTRY.exists():
            messagebox.showerror("Error", f"Entry not found:\n{VOTHA_ENTRY}")
            return
        self._stop_reader.clear()
        try:
            self.proc = subprocess.Popen(
                [PYTHON_EXE, "-u", str(VOTHA_ENTRY)],
                cwd=str(REPO_ROOT),
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=CREATE_NEW_PROCESS_GROUP
            )
            self.log_cb(f"[GUI] Started Votha (PID {self.proc.pid}).\n")
            threading.Thread(target=self._read_stdout, daemon=True).start()
        except Exception as e:
            self.log_cb(f"[GUI] Failed to start: {e}\n")
            messagebox.showerror("Start failed", str(e))

    def _read_stdout(self):
        if not self.proc or not self.proc.stdout:
            return
        for line in self.proc.stdout:
            if self._stop_reader.is_set():
                break
            self.log_cb(line)
        self.log_cb("[GUI] Votha process ended.\n")

    def stop(self):
        if not self.is_running():
            self.log_cb("[GUI] Votha is not running.\n")
            return
        try:
            if os.name == "nt":
                self.proc.terminate()
            else:
                self.proc.send_signal(signal.SIGTERM)
        except Exception as e:
            self.log_cb(f"[GUI] Terminate signal error: {e}\n")

        self._wait_exit(5)
        if self.is_running():
            self.log_cb("[GUI] Forcing kill…\n")
            try:
                self.proc.kill()
            except Exception as e:
                self.log_cb(f"[GUI] Kill error: {e}\n")

        self._stop_reader.set()
        self.proc = None
        self.log_cb("[GUI] Stopped.\n")

    def restart(self):
        self.stop()
        self.start()

    def _wait_exit(self, timeout):
        try:
            self.proc.wait(timeout=timeout)  # type: ignore[arg-type]
        except Exception:
            pass

class VothaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Votha Control Panel")
        self.geometry("860x540")
        self.minsize(720, 420)

        self.controller = VothaController(self._append)

        # --- Top Bar -------------------------------------------------------
        top = ttk.Frame(self); top.pack(fill=tk.X, padx=10, pady=(10, 6))
        ttk.Button(top, text="Start",   command=self.controller.start).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Stop",    command=self.controller.stop).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Restart", command=self.controller.restart).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Choose Config…", command=self.on_choose_config).pack(side=tk.LEFT, padx=12)
        self.status = ttk.Label(top, text="Status: Stopped"); self.status.pack(side=tk.RIGHT)

        # --- Log Area ------------------------------------------------------
        mid = ttk.Frame(self); mid.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.txt = tk.Text(mid, wrap="word", height=22)
        sc = ttk.Scrollbar(mid, orient="vertical", command=self.txt.yview)
        self.txt.configure(yscrollcommand=sc.set)
        self.txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); sc.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial info + status ticker
        self._append(f"[GUI] Repo root: {REPO_ROOT}\n[GUI] Entry: {VOTHA_ENTRY}\n")
        self.after(500, self._tick_status)

        # Close behavior
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Optional DPI fix on Windows for crisp UI
        if os.name == "nt":
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

    def on_choose_config(self):
        start_dir = REPO_ROOT / "config"
        p = filedialog.askopenfilename(
            title="Choose Votha config (JSON/JSON5)",
            initialdir=str(start_dir if start_dir.exists() else REPO_ROOT),
            filetypes=[("JSON files", "*.json *.jsonc *.json5"), ("All files", "*.*")]
        )
        if p:
            self.controller.env["VOTHA_CONFIG"] = p
            self._append(f"[GUI] Using config: {p}\n")

    def on_close(self):
        if self.controller.is_running():
            if not messagebox.askyesno("Quit", "Votha is still running. Stop it and exit?"):
                return
            self.controller.stop()
        self.destroy()

    def _append(self, text: str):
        self.txt.insert(tk.END, text)
        self.txt.see(tk.END)

    def _tick_status(self):
        self.status.config(text=f"Status: {'Running' if self.controller.is_running() else 'Stopped'}")
        self.after(500, self._tick_status)

def main():
    app = VothaGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
