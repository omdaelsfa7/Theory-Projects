class State:
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        self.transitions = {}  # symbol -> list of States

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def __repr__(self):
        return f"S{self.id}"


class NFA:
    def __init__(self, start, end):
        self.start = start  # single start state
        self.end = end      # single end/accept state

    def get_all_states(self):
        """BFS to collect all states reachable from start."""
        visited = set()
        queue = [self.start]
        while queue:
            state = queue.pop(0)
            if state.id in visited:
                continue
            visited.add(state.id)
            for symbol, targets in state.transitions.items():
                for t in targets:
                    if t.id not in visited:
                        queue.append(t)
        return visited  # set of state ids

    def get_all_states_objects(self):
        """BFS to collect all state objects reachable from start."""
        visited = {}
        queue = [self.start]
        while queue:
            state = queue.pop(0)
            if state.id in visited:
                continue
            visited[state.id] = state
            for symbol, targets in state.transitions.items():
                for t in targets:
                    if t.id not in visited:
                        queue.append(t)
        return visited  # dict id -> state

    def get_transitions(self):
        """Return list of (from_state, symbol, to_state) tuples."""
        transitions = []
        states = self.get_all_states_objects()
        for state in states.values():
            for symbol, targets in state.transitions.items():
                for t in targets:
                    transitions.append((state, symbol, t))
        return transitions
