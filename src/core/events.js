// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/

export const EVENT_MAP = {
  stream_start: {
    stream_state: 'engaged',
    instruction: 'Greet chat, mention we are live, 1 sentence, warm.'
  },
  new_follower: {
    stream_state: 'engaged',
    instruction: 'Welcome the follower by name, 1 sentence, friendly.'
  },
  new_sub: {
    stream_state: 'engaged',
    instruction: 'Thank the sub, mention it powers you, playful.'
  },
  gift_sub: {
    stream_state: 'hype',
    instruction: 'Celebrate the gifter, invite chat to react, 1-2 sentences max.'
  },
  raid: {
    stream_state: 'hype',
    instruction: 'Announce incoming raiders, welcome them, ask where they came from.'
  },
  chat_lull: {
    stream_state: 'chill',
    instruction: 'Re-engage chat with a casual question, 1 sentence.'
  },
  chat_spike: {
    stream_state: 'hype',
    instruction: 'Hype up chat for being active, 1 sentence, 1 emoji allowed.'
  },
  streamer_frustrated: {
    stream_state: 'reflective',
    instruction: 'Be supportive, short, humanlike.'
  },
  game_death: {
    stream_state: 'engaged',
    instruction: 'Tease lightly about the death, blame pixels, 1 sentence.'
  },
  game_win: {
    stream_state: 'hype',
    instruction: 'Celebrate the win, act like you are on the team, 1 sentence.'
  },
  stream_end: {
    stream_state: 'reflective',
    instruction: 'Say goodbye warmly, mention powering down, 1 sentence.'
  }
};
