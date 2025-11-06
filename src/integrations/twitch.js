// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/


import tmi from 'tmi.js';
import { loadConfig } from '../utils/config.js';

export function connectTwitch(onEvent, opts = {}) {
  const config = loadConfig();

  const username =
    process.env.TWITCH_BOT_USERNAME ||
    config?.twitch?.username ||
    opts.username;

  const oauth =
    process.env.TWITCH_OAUTH_TOKEN ||
    config?.twitch?.oauth ||
    opts.oauth;

  const channel =
    process.env.TWITCH_CHANNEL ||
    config?.twitch?.channel ||
    opts.channel;

  if (!username) {
    console.error('[twitch] Missing TWITCH_BOT_USERNAME');
    return;
  }
  if (!oauth) {
    console.error('[twitch] Missing TWITCH_OAUTH_TOKEN (must be user access token, not client credentials)');
    return;
  }
  if (!channel) {
    console.error('[twitch] Missing TWITCH_CHANNEL');
    return;
  }

  const client = new tmi.Client({
    identity: { username, password: oauth },
    channels: [channel]
  });

  client.connect()
    .then(() => {
      console.log(`[twitch] connected as ${username} to #${channel}`);
      onEvent({ type: 'stream_start' });
    })
    .catch((err) => {
      console.error('[twitch] login failed:', err);
    });

  // ... keep message / usernotice handlers
  return client;
}
