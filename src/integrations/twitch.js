import tmi from 'tmi.js';
import { loadConfig } from '../utils/config.js';

export function connectTwitch(onEvent, opts = {}) {
  const config = loadConfig();

  const {
    username = process.env.TWITCH_BOT_USERNAME,
    oauth = process.env.TWITCH_OAUTH_TOKEN,
    channel = opts.channel || config?.twitch?.channel
  } = opts;

  if (!channel) {
    console.error('[twitch] no channel specified in config.votha or env (TWITCH_CHANNEL)');
    return;
  }

  const client = new tmi.Client({
    identity: { username, password: oauth },
    channels: [channel]
  });

  client.connect()
    .then(() => {
      console.log('[twitch] connected as', username, 'to', channel);
      onEvent({ type: 'stream_start' });
    })
    .catch(console.error);

  client.on('message', (channel, tags, message, self) => {
    if (self) return;
    if (/votha/i.test(message)) {
      onEvent({
        type: 'chat_spike',
        user: tags['display-name'] || tags.username,
        text: message
      });
    }
  });

  client.on('usernotice', (channel, msg) => {
    const msgId = msg['msg-id'];
    const username = msg['display-name'] || msg.username;

    if (msgId === 'sub' || msgId === 'resub') {
      onEvent({ type: 'new_sub', user: username });
    }

    if (msgId === 'subgift') {
      onEvent({ type: 'gift_sub', user: username });
    }

    if (msgId === 'raid') {
      const viewers = msg['msg-param-viewerCount']
        ? Number(msg['msg-param-viewerCount'])
        : null;
      onEvent({ type: 'raid', user: username, amount: viewers });
    }
  });

  return client;
}
