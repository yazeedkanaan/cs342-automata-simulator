class State:
    def __init__(self, name, is_start=False, is_accept=False):
        self.name = name
        self.is_start = is_start
        self.is_accept = is_accept

        # DFA: symbol → next state
        self.transitions = {}

        # NFA: symbol → [list of next states]
        self.nfa_transitions = {}

    def add_dfa_transition(self, symbol, next_state):
        if symbol in self.transitions:
            raise ValueError(f"DFA Error: state '{self.name}' already has transition for '{symbol}'")
        self.transitions[symbol] = next_state

    def add_nfa_transition(self, symbol, next_state):
        if symbol not in self.nfa_transitions:
            self.nfa_transitions[symbol] = []
        self.nfa_transitions[symbol].append(next_state)
