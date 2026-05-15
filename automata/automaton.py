"""
automaton.py
------------
Defines the Automaton class that manages states, transitions,
and constructs DFA or NFA based on user input.
"""

from .state import State

class Automaton:
    def __init__(self, is_dfa=True):
        """
        :param is_dfa: True = DFA, False = NFA
        """
        self.states = {}
        self.start_state = None
        self.is_dfa = is_dfa

    def add_state(self, name, is_start=False, is_accept=False):
        """
        Creates a new state and adds it to the automaton.
        """
        if is_start and self.is_dfa and self.start_state is not None:
            raise ValueError("DFA Error: Only one start state allowed.")

        state = State(name, is_start, is_accept)
        self.states[name] = state

        if is_start:
            self.start_state = state

        return state

    def add_transition(self, from_state, to_state, symbol):
        """
        Adds DFA or NFA transitions based on automaton mode.
        """
        if self.is_dfa:
            self.states[from_state].add_dfa_transition(symbol,
                                                       self.states[to_state])
        else:
            self.states[from_state].add_nfa_transition(symbol,
                                                       self.states[to_state])
