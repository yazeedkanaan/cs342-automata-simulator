class LanguageGenerator:
    def generate(self, automaton, max_length, alphabet):
        simulator = __import__("automata.simulator", fromlist=["Simulator"]).Simulator()
        results = []

        def dfs(current, string):
            if len(string) > max_length:
                return
            if simulator.simulate_dfa(automaton, string) or simulator.simulate_nfa(automaton, string):
                results.append(string)
            for sym in alphabet:
                dfs(current, string + sym)

        dfs("", "")
        return sorted(set(results))
