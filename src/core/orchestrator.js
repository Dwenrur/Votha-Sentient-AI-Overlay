// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/


import { EVENT_MAP } from './events.js';
import { getState, addEvent, addLine, addNotableViewer } from './memory.js';
import { generateVothaLine } from '../ai/llm.js';
import { sendOverlayState } from '../overlay/overlay.js';
import { speak } from '../integrations/tts.js';

export async function handleEvent(evt) {
  const def = EVENT_MAP[evt.type];
  if (!def) return;

  const mem = getState();
  const context = {
    stream_state: def.stream_state || mem.stream.stream_mood || 'engaged',
    event: evt.type,
    user: evt.user || null,
    amount: evt.amount || null,
    recent_votha_lines: mem.recentLines
  };

  const rawLine = await safeGenerate(def, context);
  if (!rawLine) return;

  // clean quotes if the model adds them
  const line = rawLine.replace(/^"+|"+$/g, '').trim();

  // memory updates
  addLine(line);
  addEvent(evt);
  if (evt.user) {
    addNotableViewer(evt.user, { [evt.type]: true });
  }

  console.log('Votha:', line);

  // overlay animation
  sendOverlayState({ state: 'speaking', text: line });

  // TTS (non-blocking)
  speak(line);
}

async function safeGenerate(def, context) {
  try {
    return await generateVothaLine({
      context,
      instruction: def.instruction
    });
  } catch (err) {
    console.error('LLM error:', err);
    return fallbackLine(context);
  }
}

function fallbackLine(context) {
  switch (context.event) {
    case 'raid':
      return 'Welcome raiders! Glad you jumped in.';
    case 'new_sub':
      return 'Thanks for the support—keeps my circuits humming.';
    case 'new_follower':
      return `Welcome aboard${context.user ? ', ' + context.user : ''}.`;
    default:
      return null;
  }
}
