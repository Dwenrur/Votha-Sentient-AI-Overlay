import asyncio
import json
import websockets

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for _ in ws:
            pass  # we don’t expect messages back
    finally:
        clients.remove(ws)

async def send_overlay_update(payload):
    if not clients:
        return
    msg = json.dumps(payload)
    await asyncio.gather(*(ws.send(msg) for ws in clients))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("[Overlay] WebSocket running on ws://localhost:8765")
        await asyncio.Future()  # run forever

# allow running standalone
if __name__ == "__main__":
    asyncio.run(main())
