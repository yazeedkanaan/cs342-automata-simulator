"""
gui.py
------
Simple GUI for Automata Simulator using Tkinter.
Supports:
- Entering Regular Expression
- Building NFA (Thompson)
- Testing strings
"""

import tkinter as tk
from tkinter import messagebox

# Import automata modules
from automata.regex_parser import RegexParser
from automata.thompson import Thompson
from automata.simulator import Simulator


class AutomataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automata Simulator")
        self.root.geometry("500x400")
        self.root.config(bg="#f5f5f5")

        self.parser = RegexParser()
        self.simulator = Simulator()
        self.thompson = Thompson()
        self.nfa = None  # will store the built NFA

        self.build_widgets()

    def build_widgets(self):
        # ------------------------ Title ------------------------
        title = tk.Label(
            self.root,
            text="Automata Simulator (DFA/NFA + Regex)",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
        )
        title.pack(pady=15)

        # ------------------------ Regex input ------------------------
        tk.Label(self.root, text="Enter Regular Expression:", bg="#f5f5f5").pack()
        self.regex_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.regex_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Build NFA",
            font=("Arial", 12, "bold"),
            bg="#4a90e2",
            fg="white",
            width=15,
            command=self.build_nfa,
        ).pack(pady=5)

        # ------------------------ String test ------------------------
        tk.Label(self.root, text="Enter Test String:", bg="#f5f5f5").pack(pady=10)
        self.test_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.test_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Test String",
            font=("Arial", 12, "bold"),
            bg="#50c878",
            fg="white",
            width=15,
            command=self.test_string,
        ).pack(pady=5)

        # ------------------------ Result box ------------------------
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
        )
        self.result_label.pack(pady=20)

    # ------------------------------------------------------------
    def build_nfa(self):
        regex = self.regex_entry.get().strip()
        if not regex:
            messagebox.showerror("Error", "Please enter a regular expression.")
            return

        try:
            postfix = self.parser.to_postfix(regex)
            self.nfa = self.thompson.construct(postfix)
            messagebox.showinfo("Success", f"NFA built successfully!\nPostfix: {postfix}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------
    def test_string(self):
        if self.nfa is None:
            messagebox.showerror("Error", "Build NFA first!")
            return

        test_str = self.test_entry.get()

        accepted = self.simulator.simulate_nfa(self.nfa, test_str)

        if accepted:
            self.result_label.config(text="✔ Accepted", fg="green")
        else:
            self.result_label.config(text="✘ Rejected", fg="red")


# ------------------------------------------------------------
# Run GUI
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataGUI(root)
    root.mainloop()
