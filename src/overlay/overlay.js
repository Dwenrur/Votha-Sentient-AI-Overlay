import { startOverlayWSS } from './ws-server.js';

let overlayBus = null;

export function initOverlayServer(port = 8765) {
  overlayBus = startOverlayWSS(port);
}

export function sendOverlayState(payload) {
  if (!overlayBus) return;
  overlayBus.broadcast(payload);
}
