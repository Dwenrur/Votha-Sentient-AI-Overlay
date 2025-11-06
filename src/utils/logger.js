// Copyright (c) 2025 [Elijah Purvey]
// Licensed under the PolyForm Noncommercial License 1.0.0
// https://polyformproject.org/licenses/noncommercial/1.0.0/


export function log(type, message, ...extra) {
  const prefix = `[${new Date().toISOString()}][${type.toUpperCase()}]`;
  console.log(prefix, message, ...extra);
}

export const logger = {
  info: (msg, ...e) => log('info', msg, ...e),
  warn: (msg, ...e) => log('warn', msg, ...e),
  error: (msg, ...e) => log('error', msg, ...e)
};
