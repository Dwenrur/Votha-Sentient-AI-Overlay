import { initStream } from '../core/memory.js';
import { initOverlayServer } from '../overlay/overlay.js';
import { handleEvent } from '../core/orchestrator.js';
import { connectTwitch } from '../integrations/twitch.js';
import { loadConfig } from '../utils/config.js';

const config = loadConfig();
const overlayPort =
  (config.overlay && (config.overlay.port || getPortFromWs(config.overlay.ws_url))) ||
  8765;

// start memory + overlay
initStream(`stream-${Date.now()}`, null);
initOverlayServer(overlayPort);

// connect to the single channel
connectTwitch(handleEvent);

// (optional) mock events
// ...

function getPortFromWs(wsUrl) {
  if (!wsUrl) return null;
  try {
    const u = new URL(wsUrl);
    return Number(u.port) || 8765;
  } catch {
    return 8765;
  }
}
