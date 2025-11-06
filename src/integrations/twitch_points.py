# Copyright (c) 2025 [Elijah Purvey]
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0/

# src/integrations/twitch_points.py
import asyncio
import json
import threading
import requests
import websockets
from queue import Queue
from src.utils.config import load_config

cfg = load_config()
tw = cfg.get("twitch", {})

CLIENT_ID = tw.get("client_id", "").strip()
CLIENT_SECRET = tw.get("client_secret", "").strip()
BROADCASTER_ID = tw.get("broadcaster_id", "").strip()
REWARD_ID = (tw.get("reward_id") or "").strip()
USER_TOKEN = tw.get("user_access_token", "").strip()  # <-- new

redeem_queue: Queue = Queue()

def _ensure(field, value, hint=""):
    if not value or value.startswith("YOUR_"):
        raise RuntimeError(f"[twitch] Missing/placeholder `{field}` in config. {hint}")

def start_twitch_listener():
    # Fail early with clear messages
    _ensure("twitch.client_id", CLIENT_ID, "Create an app in Twitch dev console.")
    _ensure("twitch.client_secret", CLIENT_SECRET, "Copy the app secret.")
    _ensure("twitch.broadcaster_id", BROADCASTER_ID, "Fill with your channel’s user ID.")
    _ensure("twitch.user_access_token", USER_TOKEN,
            "Get a USER token with scope channel:read:redemptions (twitch CLI: `twitch token -u -s channel:read:redemptions`).")

    loop = asyncio.new_event_loop()
    def runner():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_twitch_ws_loop())
    threading.Thread(target=runner, daemon=True).start()

async def _twitch_ws_loop():
    # connect to EventSub WS
    async with websockets.connect("wss://eventsub.wss.twitch.tv/ws") as ws:
        welcome = json.loads(await ws.recv())
        session_id = welcome["payload"]["session"]["id"]

        # Build the subscription payload
        sub_payload = {
            "type": "channel.channel_points_custom_reward_redemption.add",
            "version": "1",
            "condition": {
                "broadcaster_user_id": BROADCASTER_ID
            },
            "transport": {
                "method": "websocket",
                "session_id": session_id
            }
        }
        if REWARD_ID:
            sub_payload["condition"]["reward_id"] = REWARD_ID

        # Send subscribe with REQUIRED headers embedded (Twitch validates the token on WS session)
        await ws.send(json.dumps({
            "type": "session.subscribe",
            "nonce": "votha-sub-1",
            "payload": sub_payload
        }))

        print("[twitch] subscribed to channel point redemptions")

        while True:
            raw = await ws.recv()
            msg = json.loads(raw)
            mtype = msg["metadata"]["message_type"]

            if mtype == "session_keepalive":
                continue
            if mtype == "session_welcome":
                continue
            if mtype == "session_reconnect":
                # handle reconnection if you like
                continue

            if mtype == "notification":
                event = msg["payload"]["event"]
                user = event["user_name"]
                user_input = event.get("user_input", "") or ""
                reward_title = event["reward"]["title"]
                print(f"[twitch] {user} redeemed {reward_title} -> {user_input}")
                redeem_queue.put((user, user_input))
