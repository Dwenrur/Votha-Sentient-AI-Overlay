import { WebSocketServer } from 'ws';

export function startOverlayWSS(port = 8765) {
  const wss = new WebSocketServer({ port });
  console.log(`[overlay-ws] listening on ws://localhost:${port}`);

  function broadcast(data) {
    const msg = typeof data === 'string' ? data : JSON.stringify(data);
    wss.clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(msg);
      }
    });
  }

  return { broadcast };
}
