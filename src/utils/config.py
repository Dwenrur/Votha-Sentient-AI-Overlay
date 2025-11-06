# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/


import json
import os
from pathlib import Path

def load_config() -> dict:
    """
    Loads the main configuration file for Votha.
    Expected location:
      <project_root>/config/votha-config.json
    You can override it by setting the VOTHA_CONFIG environment variable.
    """
    # 1) Environment override (for custom setups)
    override = os.environ.get("VOTHA_CONFIG")
    if override:
        path = Path(override)
        if path.is_file():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"VOTHA_CONFIG points to missing file: {path}")

    # 2) Default expected location
    root_dir = Path(__file__).resolve().parents[2]
    cfg_path = root_dir / "config" / "votha-config.json"

    if not cfg_path.is_file():
        raise FileNotFoundError(
            f"Votha config not found at expected path:\n  {cfg_path}\n"
            "Please ensure it exists and is named 'votha-config.json'."
        )

    with cfg_path.open("r", encoding="utf-8") as f:
        return json.load(f)
