from automata.automaton import Automaton
from automata.simulator import Simulator
from automata.regex_parser import RegexParser
from automata.thompson import Thompson

print("=== Automata Simulator ===")
regex = input("Enter regular expression: ")

parser = RegexParser()
postfix = parser.to_postfix(regex)

print("Postfix:", postfix)

th = Thompson()
nfa = th.construct(postfix)

sim = Simulator()

while True:
    s = input("Enter string to test (or 'exit'): ")
    if s == "exit":
        break
    print("Accepted" if sim.simulate_nfa(nfa, s) else "Rejected")
