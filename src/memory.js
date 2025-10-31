const state = {
  stream: {
    id: null,
    current_game: null,
    stream_mood: 'engaged'
  },
  recentEvents: [],
  recentLines: [],
  notableViewers: {}
};

export function initStream(id, game = null) {
  state.stream.id = id;
  state.stream.current_game = game;
  state.recentEvents = [];
  state.recentLines = [];
  state.notableViewers = {};
}

export function addEvent(evt) {
  state.recentEvents.unshift(evt);
  state.recentEvents = state.recentEvents.slice(0, 10);
}

export function addLine(line) {
  state.recentLines.unshift(line);
  state.recentLines = state.recentLines.slice(0, 10);
}

export function addNotableViewer(name, data) {
  state.notableViewers[name] = {
    ...(state.notableViewers[name] || {}),
    ...data
  };
}

export function getState() {
  return state;
}
