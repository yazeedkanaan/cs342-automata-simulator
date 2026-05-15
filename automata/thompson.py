"""
thompson.py
-----------
Implements Thompson’s construction algorithm to convert
postfix regular expressions into NFAs.
"""

from .automaton import Automaton

class Thompson:
    counter = 0

    def new_state(self):
        """ Creates unique state names. """
        name = f"S{Thompson.counter}"
        Thompson.counter += 1
        return name

    def construct(self, postfix):
        """
        Builds an NFA from postfix expression using a stack-based approach.
        """
        stack = []

        for char in postfix:
            # -------------------- Basic symbol --------------------
            if char.isalnum():
                nfa = Automaton(is_dfa=False)
                s = nfa.add_state(self.new_state(), is_start=True)
                e = nfa.add_state(self.new_state(), is_accept=True)
                s.add_nfa_transition(char, e)
                stack.append(nfa)

            # -------------------- Concatenation --------------------
            elif char == ".":
                nfa2 = stack.pop()
                nfa1 = stack.pop()

                # Connect accepts of nfa1 to start of nfa2
                for st in nfa1.states.values():
                    if st.is_accept:
                        st.add_nfa_transition("", nfa2.start_state)
                        st.is_accept = False

                # merge
                nfa1.states.update(nfa2.states)
                stack.append(nfa1)

            # -------------------- Union --------------------
            elif char == "|":
                nfa2 = stack.pop()
                nfa1 = stack.pop()

                nfa = Automaton(is_dfa=False)
                s = nfa.add_state(self.new_state(), is_start=True)
                e = nfa.add_state(self.new_state(), is_accept=True)

                s.add_nfa_transition("", nfa1.start_state)
                s.add_nfa_transition("", nfa2.start_state)

                for st in nfa1.states.values():
                    if st.is_accept:
                        st.add_nfa_transition("", e)
                        st.is_accept = False

                for st in nfa2.states.values():
                    if st.is_accept:
                        st.add_nfa_transition("", e)
                        st.is_accept = False

                nfa.states.update(nfa1.states)
                nfa.states.update(nfa2.states)
                nfa.states[s.name] = s
                nfa.states[e.name] = e
                stack.append(nfa)

            # -------------------- Kleene Star --------------------
            elif char == "*":
                nfa1 = stack.pop()

                nfa = Automaton(is_dfa=False)
                s = nfa.add_state(self.new_state(), is_start=True)
                e = nfa.add_state(self.new_state(), is_accept=True)

                s.add_nfa_transition("", nfa1.start_state)
                s.add_nfa_transition("", e)

                for st in nfa1.states.values():
                    if st.is_accept:
                        st.add_nfa_transition("", nfa1.start_state)
                        st.add_nfa_transition("", e)
                        st.is_accept = False

                nfa.states.update(nfa1.states)
                nfa.states[s.name] = s
                nfa.states[e.name] = e

                stack.append(nfa)

        return stack.pop()
