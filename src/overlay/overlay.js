// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/


import { startOverlayWSS } from './ws-server.js';

let overlayBus = null;

export function initOverlayServer(port = 8765) {
  overlayBus = startOverlayWSS(port);
}

export function sendOverlayState(payload) {
  if (!overlayBus) return;
  overlayBus.broadcast(payload);
}
