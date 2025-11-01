import fetch from 'node-fetch';
import { loadConfig } from '../utils/config.js';

const cfg = loadConfig();
const TTS_ENABLED = cfg?.tts?.enabled ?? false;
const TTS_URL = cfg?.tts?.url || 'http://localhost:5002/tts';
const TTS_VOICE = cfg?.tts?.voice || 'votha';

export async function speak(text) {
  if (!TTS_ENABLED) return;
  if (!text) return;

  try {
    await fetch(TTS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        voice: TTS_VOICE
      })
    });
  } catch (err) {
    console.warn('[tts] failed to speak:', err.message);
  }
}
