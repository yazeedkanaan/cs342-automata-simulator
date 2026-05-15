c"""
state.py
---------
Defines the State class used in DFA and NFA constructions.
Each state may contain deterministic transitions (DFA)
and non-deterministic transitions including epsilon (NFA).
"""

class State:
    def __init__(self, name, is_start=False, is_accept=False):
        """
        :param name: Unique state name (string)
        :param is_start: True if this is the start state
        :param is_accept: True if this is an accepting state
        """
        self.name = name
        self.is_start = is_start
        self.is_accept = is_accept

        # deterministic transitions → for DFA
        self.transitions = {}

        # nondeterministic transitions → for NFA (symbol: list of states)
        self.nfa_transitions = {}

    def add_dfa_transition(self, symbol, next_state):
        """
        Adds deterministic transition for DFA.

        :param symbol: input symbol
        :param next_state: next State object
        """
        if symbol in self.transitions:
            raise ValueError(f"DFA Error: State '{self.name}' "
                             f"already has a transition for '{symbol}'.")
        self.transitions[symbol] = next_state

    def add_nfa_transition(self, symbol, next_state):
        """
        Adds nondeterministic transition for NFA.

        :param symbol: input symbol or epsilon ""
        :param next_state: next State object
        """
        self.nfa_transitions.setdefault(symbol, []).append(next_state)
