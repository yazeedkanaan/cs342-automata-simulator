"""
gui.py
------
Enhanced GUI for Automata Simulator using Tkinter.
Supports: Regex to NFA and String Testing with DFA Constraint Testing.
"""

import tkinter as tk
from tkinter import messagebox, ttk

# Import automata modules
from automata.regex_parser import RegexParser
from automata.thompson import Thompson
from automata.simulator import Simulator
from automata.automaton import Automaton


class AutomataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CS342 - Automata Simulator & Regex Processor")
        self.root.geometry("650x550")
        self.root.config(bg="#f4f6f9")

        self.parser = RegexParser()
        self.simulator = Simulator()
        self.thompson = Thompson()
        self.nfa = None  # stores the built NFA

        self.build_widgets()

    def build_widgets(self):
        # ------------------------ Main Title ------------------------
        title = tk.Label(
            self.root,
            text="Automata Simulator & Processor",
            font=("Helvetica", 16, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50"
        )
        title.pack(pady=15)

        # Create notebook for tabs (Regex Mode & Custom DFA Mode)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Regex & NFA Simulation")
        notebook.add(tab2, text="DFA Constraint Verification")

        self.setup_regex_tab(tab1)
        self.setup_dfa_tab(tab2)

    def setup_regex_tab(self, frame):
        # ------------------------ Regex input ------------------------
        lbl_frame1 = tk.LabelFrame(frame, text=" 1. Regex to NFA Construction ", font=("Arial", 11, "bold"), padx=10, pady=10)
        lbl_frame1.pack(fill="x", padx=10, pady=5)

        tk.Label(lbl_frame1, text="Enter Regular Expression (e.g., (a|b)*abb ):", font=("Arial", 10)).pack(anchor="w")
        self.regex_entry = tk.Entry(lbl_frame1, width=50, font=("Arial", 11))
        self.regex_entry.pack(pady=5, fill="x")

        tk.Button(
            lbl_frame1, text="Build NFA (Thompson)", font=("Arial", 11, "bold"),
            bg="#3498db", fg="white", command=self.build_nfa
        ).pack(pady=5)

        # ------------------------ String test ------------------------
        lbl_frame2 = tk.LabelFrame(frame, text=" 2. Simulation Engine (Test String) ", font=("Arial", 11, "bold"), padx=10, pady=10)
        lbl_frame2.pack(fill="x", padx=10, pady=5)

        tk.Label(lbl_frame2, text="Enter String to Verify:", font=("Arial", 10)).pack(anchor="w")
        self.test_entry = tk.Entry(lbl_frame2, width=50, font=("Arial", 11))
        self.test_entry.pack(pady=5, fill="x")

        tk.Button(
            lbl_frame2, text="Simulate & Test", font=("Arial", 11, "bold"),
            bg="#2ecc71", fg="white", command=self.test_string
        ).pack(pady=5)

        self.result_label = tk.Label(lbl_frame2, text="Status: Waiting for Input", font=("Arial", 12, "bold"), fg="#7f8c8d")
        self.result_label.pack(pady=5)

    def setup_dfa_tab(self, frame):
        lbl_dfa = tk.LabelFrame(frame, text=" Demonstration of DFA Rules & Constraint Enforcement ", font=("Arial", 11, "bold"), padx=10, pady=10)
        lbl_dfa.pack(fill="both", expand=True, padx=10, pady=10)

        desc = (
            "According to DFA constraints, an automaton can only have ONE start state, "
            "and MUST NOT have duplicate deterministic transitions for the same symbol from any single state.\n\n"
            "Click the buttons below to see how the engine enforces these rules and rejects invalid designs dynamically."
        )
        tk.Label(lbl_dfa, text=desc, justify="left", wraplength=550, font=("Arial", 10), fg="#34495e").pack(pady=10)

        tk.Button(
            lbl_dfa, text="Test Constraint 1: Multiple Start States Error", font=("Arial", 10, "bold"),
            bg="#e74c3c", fg="white", width=45, command=self.test_dfa_start_constraint
        ).pack(pady=10)

        tk.Button(
            lbl_dfa, text="Test Constraint 2: Ambiguous/Duplicate Transition Error", font=("Arial", 10, "bold"),
            bg="#e74c3c", fg="white", width=45, command=self.test_dfa_transition_constraint
        ).pack(pady=10)

        tk.Button(
            lbl_dfa, text="Test Success: Construct & Run a Valid DFA", font=("Arial", 10, "bold"),
            bg="#27ae60", fg="white", width=45, command=self.test_valid_dfa
        ).pack(pady=10)

        self.dfa_status = tk.Label(lbl_dfa, text="", font=("Arial", 11, "italic"), fg="#2c3e50")
        self.dfa_status.pack(pady=15)

    # ------------------------------------------------------------
    def build_nfa(self):
        regex = self.regex_entry.get().strip()
        if not regex:
            messagebox.showerror("Error", "Please enter a regular expression.")
            return

        try:
            postfix = self.parser.to_postfix(regex)
            self.nfa = self.thompson.construct(postfix)
            messagebox.showinfo("Success", f"NFA built successfully via Thompson's Construction!\nPostfix Notation: {postfix}")
        except Exception as e:
            messagebox.showerror("Error", f"Parsing Error: {str(e)}")

    def test_string(self):
        if self.nfa is None:
            messagebox.showerror("Error", "Please build the NFA from a regular expression first!")
            return

        test_str = self.test_entry.get()
        accepted = self.simulator.simulate_nfa(self.nfa, test_str)

        if accepted:
            self.result_label.config(text=f"✔ Accepted: '{test_str}' belongs to the language.", fg="#27ae60")
        else:
            self.result_label.config(text=f"✘ Rejected: '{test_str}' does not belong to the language.", fg="#c0392b")

    # ------------------------------------------------------------
    # Constraint Enforcement Testing Functions
    # ------------------------------------------------------------
    def test_dfa_start_constraint(self):
        try:
            dfa = Automaton(is_dfa=True)
            dfa.add_state("Q0", is_start=True)
            dfa.add_state("Q1", is_start=True) 
        except ValueError as e:
            self.dfa_status.config(text=f"Caught Enforced Exception:\n{str(e)}", fg="#c0392b")
            messagebox.showinfo("Constraint Verified", f"Success! Engine blocked multiple start states:\n\n{str(e)}")

    def test_dfa_transition_constraint(self):
        try:
            dfa = Automaton(is_dfa=True)
            dfa.add_state("Q0", is_start=True)
            dfa.add_state("Q1", is_accept=True)
            dfa.add_transition("Q0", "Q1", "a")
            dfa.add_transition("Q0", "Q1", "a")
        except ValueError as e:
            self.dfa_status.config(text=f"Caught Enforced Exception:\n{str(e)}", fg="#c0392b")
            messagebox.showinfo("Constraint Verified", f"Success! Engine blocked ambiguous duplicate transition:\n\n{str(e)}")

    def test_valid_dfa(self):
        try:
            dfa = Automaton(is_dfa=True)
            dfa.add_state("Q0", is_start=True)
            dfa.add_state("Q1", is_accept=True)
            dfa.add_transition("Q0", "Q1", "a")
            dfa.add_transition("Q1", "Q1", "a")
            dfa.add_transition("Q1", "Q1", "b")
            
            res1 = self.simulator.simulate_dfa(dfa, "aab")
            res2 = self.simulator.simulate_dfa(dfa, "bb")
            
            status_text = f"Valid DFA Constructed Successfully!\nSimulating over alphabet {{a, b}}:\n'aab' -> {'Accepted' if res1 else 'Rejected'}\n'bb' -> {'Accepted' if res2 else 'Rejected'}"
            self.dfa_status.config(text=status_text, fg="#27ae60")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataGUI(root)
    root.mainloop()
