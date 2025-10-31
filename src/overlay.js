import WebSocket from 'ws';

let ws = null;

export function initOverlay(url) {
  try {
    ws = new WebSocket(url);
    ws.on('open', () => console.log('[overlay] connected'));
    ws.on('close', () => console.log('[overlay] disconnected'));
  } catch (err) {
    console.warn('[overlay] cannot connect', err.message);
  }
}

export function sendOverlayState(payload) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  }
}
