import { initStream } from './memory.js';
import { initOverlay } from './overlay.js';
import { handleEvent } from './orchestrator.js';

// init stream session
initStream(`stream-${Date.now()}`, null);

// connect overlay (optional)
initOverlay('ws://localhost:8765');

// TODO: hook to real Twitch events here
// for now, simulate a few events
setTimeout(() => {
  handleEvent({ type: 'stream_start' });
}, 500);

setTimeout(() => {
  handleEvent({ type: 'new_follower', user: 'NovaByte' });
}, 1500);

setTimeout(() => {
  handleEvent({ type: 'raid', user: 'PixelPirates', amount: 27 });
}, 3000);
