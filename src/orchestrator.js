import { EVENT_MAP } from './events.js';
import { getState, addEvent, addLine, addNotableViewer } from './memory.js';
import { generateVothaLine } from './llm.js';
import { sendOverlayState } from './overlay.js';

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

  const line = await safeGenerate(def, context);

  if (line) {
    addLine(line);
    addEvent(evt);
    if (evt.user) {
      addNotableViewer(evt.user, { [evt.type]: true });
    }

    console.log('Votha:', line);
    sendOverlayState({ state: 'speaking', text: line });
  }
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
