// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/


import fetch from 'node-fetch';
import { loadConfig } from '../utils/config.js';

const cfg = loadConfig();

// env overrides
const TTS_ENABLED = process.env.TTS_ENABLED === 'true'
  || cfg?.tts?.enabled === true;

const TTS_MODE = process.env.TTS_MODE || cfg?.tts?.mode || 'local';

// local/default
const TTS_URL = process.env.TTS_URL || cfg?.tts?.url || 'http://localhost:5002/tts';
const TTS_VOICE = process.env.TTS_VOICE || cfg?.tts?.voice || 'votha';

// elevenlabs
const ELEVEN_API_KEY = process.env.ELEVENLABS_API_KEY || cfg?.tts?.elevenlabs_api_key;
const ELEVEN_VOICE_ID = process.env.ELEVENLABS_VOICE_ID || cfg?.tts?.elevenlabs_voice_id;

export async function speak(text) {
  if (!TTS_ENABLED) return;
  if (!text) return;

  try {
    if (TTS_MODE === 'elevenlabs') {
      await speakElevenLabs(text);
    } else {
      await speakLocal(text);
    }
  } catch (err) {
    console.warn('[tts] failed:', err.message);
  }
}

async function speakLocal(text) {
  // simplest possible shape: { text, voice }
  const res = await fetch(TTS_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      voice: TTS_VOICE
    })
  });

  if (!res.ok) {
    const body = await res.text();
    console.warn('[tts] local tts error:', res.status, body);
  }
}

// simple ElevenLabs integration
async function speakElevenLabs(text) {
  if (!ELEVEN_API_KEY || !ELEVEN_VOICE_ID) {
    console.warn('[tts] elevenlabs missing API key or voice id');
    return;
  }

  // this one returns audio; usually you'd play it on the client,
  // but for now we just trigger it. later we can write to a file or stream.
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${ELEVEN_VOICE_ID}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': ELEVEN_API_KEY,
      'accept': 'audio/mpeg'
    },
    body: JSON.stringify({
      text,
      model_id: 'eleven_multilingual_v2'
    })
  });

  if (!res.ok) {
    const body = await res.text();
    console.warn('[tts] elevenlabs error:', res.status, body);
  }
}
