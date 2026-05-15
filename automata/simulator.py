class Simulator:
    # DFA Simulation --------------------------
    def simulate_dfa(self, automaton, input_string):
        current = automaton.start_state

        for symbol in input_string:
            if symbol not in current.transitions:
                return False
            current = current.transitions[symbol]

        return current.is_accept

    # NFA Simulation --------------------------
    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            if "" in state.nfa_transitions:
                for next_state in state.nfa_transitions[""]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def simulate_nfa(self, automaton, input_string):
        current_states = self.epsilon_closure([automaton.start_state])

        for symbol in input_string:
            next_states = set()

            for state in current_states:
                if symbol in state.nfa_transitions:
                    for next_state in state.nfa_transitions[symbol]:
                        next_states.update(self.epsilon_closure([next_state]))

            current_states = next_states

        return any(s.is_accept for s in current_states)
