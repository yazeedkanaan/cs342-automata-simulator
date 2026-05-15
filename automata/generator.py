"""
generator.py
-------------
Generates all accepted strings up to max_length.
Supports DFA & NFA.
"""

from .simulator import Simulator

class LanguageGenerator:
    def generate(self, automaton, max_length, alphabet):
        """
        Generates all accepted strings up to a given length.
        """
        simulator = Simulator()
        results = set()

        def dfs(current_string):
            if len(current_string) > max_length:
                return

            # test the string
            if automaton.is_dfa:
                accepted = simulator.simulate_dfa(automaton, current_string)
            else:
                accepted = simulator.simulate_nfa(automaton, current_string)

            if accepted:
                results.add(current_string)

            # expand
            for sym in alphabet:
                dfs(current_string + sym)

        dfs("")
        return sorted(results)
