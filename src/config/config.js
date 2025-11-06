import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let cachedConfig = null;

export function loadConfig() {
  if (cachedConfig) return cachedConfig;

  const configPath = path.resolve(__dirname, '../../config/votha.config.json');

  let raw = '{}';
  try {
    raw = fs.readFileSync(configPath, 'utf-8');
  } catch (err) {
    console.warn('[config] could not read config/votha.config.json, using defaults');
  }

  const json = JSON.parse(raw);

  // simple env overrides, still useful
  if (process.env.VOTHA_PORT) {
    json.overlay = json.overlay || {};
    json.overlay.port = Number(process.env.VOTHA_PORT);
    json.overlay.ws_url = `ws://localhost:${process.env.VOTHA_PORT}`;
  }

  if (process.env.VOTHA_MODEL) {
    json.model = json.model || {};
    json.model.name = process.env.VOTHA_MODEL;
  }

  if (process.env.TWITCH_CHANNEL) {
    json.twitch = json.twitch || {};
    json.twitch.channel = process.env.TWITCH_CHANNEL;
  }

  cachedConfig = json;
  return json;
}