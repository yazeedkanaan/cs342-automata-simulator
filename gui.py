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
            "Click the buttons below to see how the engine enforces these rules and rejects invalid designs dynamically
