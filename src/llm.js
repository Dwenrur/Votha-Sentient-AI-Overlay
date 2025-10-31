import fetch from 'node-fetch';

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

export async function generateVothaLine({ context, instruction, model = 'llama3.2:8b' }) {
  const messages = [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'user', content: buildUserPrompt(context, instruction) }
  ];

  const res = await fetch('http://localhost:11434/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      messages,
      stream: false,
      temperature: 0.7,
      top_p: 0.9,
      max_tokens: 40
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
