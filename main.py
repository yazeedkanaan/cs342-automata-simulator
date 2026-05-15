from automata.regex_parser import RegexParser
from automata.thompson import Thompson
from automata.simulator import Simulator

def main():
    print("=== Automata Simulator ===")

    regex = input("Enter Regular Expression: ")

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

        accepted = sim.simulate_nfa(nfa, s)
        print("Accepted" if accepted else "Rejected")

if __name__ == "__main__":
    main()
