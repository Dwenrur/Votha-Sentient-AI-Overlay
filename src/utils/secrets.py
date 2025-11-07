# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# src/utils/secrets.py
from __future__ import annotations
import keyring

SERVICE = "Votha"

def get_secret(key: str) -> str | None:
    try:
        return keyring.get_password(SERVICE, key)
    except Exception:
        return None

def set_secret(key: str, value: str | None):
    try:
        if value:
            keyring.set_password(SERVICE, key, value)
        else:
            # remove if set to empty/None
            keyring.delete_password(SERVICE, key)
    except keyring.errors.PasswordDeleteError:
        pass
    except Exception:
        pass
