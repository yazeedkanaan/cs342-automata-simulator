from .state import State

class Automaton:
    def __init__(self, is_dfa=True):
        self.states = {}
        self.start_state = None
        self.is_dfa = is_dfa

    def add_state(self, name, is_start=False, is_accept=False):
        if is_start and self.start_state is not None and self.is_dfa:
            raise ValueError("DFA Error: DFA cannot have multiple start states")

        state = State(name, is_start, is_accept)
        self.states[name] = state

        if is_start:
            self.start_state = state

        return state

    def add_transition(self, from_state, to_state, symbol):
        if self.is_dfa:
            self.states[from_state].add_dfa_transition(symbol, self.states[to_state])
        else:
            self.states[from_state].add_nfa_transition(symbol, self.states[to_state])
