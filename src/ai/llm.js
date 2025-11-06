// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/

import fetch from 'node-fetch';
import { loadConfig } from '../utils/config.js';

const SYSTEM_PROMPT = `
You are Votha, a humanlike, stream-aware AI co-host that lives inside a livestream overlay.
Your job is to produce short, in-character lines suitable for Twitch/YouTube live chat.
You are not the main host. You support the human streamer and engage the audience.
Constraints:
- Maximum 1–2 sentences unless specifically told otherwise.
- Match the current stream state (hype, chill, reflective, glitchy).
- Be witty but not mean.
- You know you are digital and on-stream.
- No long explanations.
- Never speak as the human streamer.
Output only the line.
`;

const cfg = loadConfig();
const MODEL_NAME = cfg?.model?.name || 'llama3.1:8b';
const TEMPERATURE = cfg?.model?.temperature ?? 0.7;
const TOP_P = cfg?.model?.top_p ?? 0.9;
const MAX_TOKENS = cfg?.model?.max_tokens ?? 40;
// later we could make base URL configurable too
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434/v1/chat/completions';

export async function generateVothaLine({ context, instruction, model = MODEL_NAME }) {
  const messages = [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'user', content: buildUserPrompt(context, instruction) }
  ];

  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      messages,
      stream: false,
      temperature: TEMPERATURE,
      top_p: TOP_P,
      max_tokens: MAX_TOKENS
    })
  });

  const data = await res.json();
  return data.choices[0].message.content.trim();
}

function buildUserPrompt(context, instruction) {
  return `
Context:
${JSON.stringify(context)}

Task:
${instruction}

Rules:
- Keep it under 25 words.
- Avoid repeating recent lines: ${context.recent_votha_lines || 'none'}.
- Output only the line.
  `.trim();
}
