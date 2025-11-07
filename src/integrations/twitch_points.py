# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# src/integrations/twitch_points.py
import asyncio
import json
import threading
import time
from typing import Optional

import requests
import websockets
from websockets.exceptions import ConnectionClosed

from queue import Queue
from src.utils.config import load_config

cfg = load_config()
tw = cfg.get("twitch", {})

CLIENT_ID = (tw.get("client_id") or "").strip()
CLIENT_SECRET = (tw.get("client_secret") or "").strip()
BROADCASTER_ID = (tw.get("broadcaster_id") or "").strip()
REWARD_ID = (tw.get("reward_id") or "").strip()
USER_TOKEN = (tw.get("user_access_token") or "").strip()  # user token w/ scope channel:read:redemptions

redeem_queue: Queue = Queue()

EVENTSUB_WS = "wss://eventsub.wss.twitch.tv/ws"
HELIX_SUBS = "https://api.twitch.tv/helix/eventsub/subscriptions"

# ---------- utilities ----------

def _ensure(field: str, value: str, hint: str = ""):
    if not value or value.startswith("YOUR_"):
        raise RuntimeError(f"[twitch] Missing/placeholder `{field}` in config. {hint}")

def _helix_headers(include_json: bool = False):
    h = {
        "Client-Id": CLIENT_ID,
        "Authorization": f"Bearer {USER_TOKEN}",
    }
    if include_json:
        h["Content-Type"] = "application/json"
    return h

def _clear_old_redemption_subs():
    """Remove older/duplicate subs so restarts don’t accumulate them."""
    try:
        r = requests.get(HELIX_SUBS, headers=_helix_headers())
        r.raise_for_status()
        for sub in r.json().get("data", []):
            if (
                sub.get("type") == "channel.channel_points_custom_reward_redemption.add"
                and sub.get("condition", {}).get("broadcaster_user_id") == BROADCASTER_ID
            ):
                sid = sub.get("id")
                try:
                    requests.delete(f"{HELIX_SUBS}?id={sid}", headers=_helix_headers())
                    print(f"[twitch] removed old subscription {sid}")
                except Exception as e:
                    print(f"[twitch] warn: failed to remove sub {sid}: {e}")
    except Exception as e:
        print(f"[twitch] warn: listing subscriptions failed: {e}")

def _create_redemption_subscription(session_id: str):
    payload = {
        "type": "channel.channel_points_custom_reward_redemption.add",
        "version": "1",
        "condition": {"broadcaster_user_id": BROADCASTER_ID},
        "transport": {"method": "websocket", "session_id": session_id},
    }
    if REWARD_ID:
        payload["condition"]["reward_id"] = REWARD_ID

    r = requests.post(HELIX_SUBS, headers=_helix_headers(include_json=True), json=payload)
    if r.status_code in (401, 403):
        raise RuntimeError(
            "[twitch] Auth failed creating EventSub subscription. "
            "Use a *user* token with scope: channel:read:redemptions."
        )
    if not r.ok:
        raise RuntimeError(f"[twitch] Subscription failed: {r.status_code} {r.text}")

    print("[twitch] subscribed to channel point redemptions (EventSub over WS)")

# ---------- main async loop ----------

async def _receive_notifications(ws: websockets.WebSocketClientProtocol):
    """Receive-only loop. Do not send arbitrary frames on EventSub WS."""
    while True:
        raw = await ws.recv()
        msg = json.loads(raw)
        mtype = (msg.get("metadata") or {}).get("message_type") or msg.get("type")

        if mtype in ("session_keepalive", "session_welcome"):
            continue

        if mtype == "session_reconnect":
            # The server is instructing us to reconnect to a new URL.
            url = msg["payload"]["session"]["reconnect_url"]
            print(f"[twitch] session_reconnect -> {url}")
            return url  # signal caller to hop

        if mtype == "notification":
            event = msg["payload"]["event"]
            user = event.get("user_name") or event.get("user_login") or "unknown"
            user_input = event.get("user_input") or ""
            reward = (event.get("reward") or {}).get("title") or "Channel Points Redemption"
            print(f"[twitch] {user} redeemed {reward} -> {user_input}")
            redeem_queue.put((user, user_input))

        # Unknown message types are ignored but logged once for visibility
        else:
            kind = msg.get("metadata", {}).get("message_type") or msg.get("type")
            print(f"[twitch] info: unhandled message type: {kind}")

async def _connect_and_listen(start_url: str = EVENTSUB_WS):
    """
    Connect to EventSub WS, register subscription via Helix, and process messages.
    Handles server-directed reconnects and transient failures with backoff.
    """
    url: Optional[str] = start_url
    backoff = 1.0

    while True:
        try:
            async with websockets.connect(url) as ws:
                # Wait for welcome to get session id
                welcome = json.loads(await ws.recv())
                session = welcome["payload"]["session"]
                session_id = session["id"]

                # Best effort: clear prior subs (prevents duplicates on restarts)
                _clear_old_redemption_subs()

                # Register this session id via Helix
                _create_redemption_subscription(session_id)

                # Reset backoff upon successful connection+subscription
                backoff = 1.0

                # Receive-only loop; may return a reconnect URL
                next_url = await _receive_notifications(ws)
                if next_url:
                    url = next_url
                    continue

        except ConnectionClosed as e:
            print(f"[twitch] connection closed ({e.code}): {e}. Reconnecting soon...")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"[twitch] error: {e}")

        # Exponential backoff with a cap
        time.sleep(backoff)
        backoff = min(backoff * 2.0, 60.0)

# ---------- public API ----------

def start_twitch_listener():
    # Fail early with clear messages
    _ensure("twitch.client_id", CLIENT_ID, "Create an app in Twitch dev console.")
    _ensure("twitch.client_secret", CLIENT_SECRET, "Copy the app secret.")
    _ensure("twitch.broadcaster_id", BROADCASTER_ID, "Fill with your channel’s user ID.")
    _ensure(
        "twitch.user_access_token",
        USER_TOKEN,
        "Get a USER token with scope channel:read:redemptions "
        "(twitch CLI: `twitch token -u -s channel:read:redemptions`).",
    )

    loop = asyncio.new_event_loop()

    def runner():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_connect_and_listen())

    threading.Thread(target=runner, daemon=True).start()
