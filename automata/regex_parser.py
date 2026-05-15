"""
regex_parser.py
----------------
Converts regular expressions into postfix notation
using the Shunting Yard algorithm.
"""

class RegexParser:
    # Operator precedence
    precedence = {
        "*": 3,
        ".": 2,
        "|": 1
    }

    def add_concat(self, regex):
        """
        Automatically inserts concatenation operator '.' when needed.
        """
        result = ""
        for i in range(len(regex)):
            result += regex[i]

            if i + 1 < len(regex):
                if (regex[i] not in "(|") and (regex[i+1] not in "*)|"):
                    result += "."
        return result

    def to_postfix(self, regex):
        """
        Converts infix regex to postfix using Shunting Yard.
        """
        regex = self.add_concat(regex)
        output = ""
        stack = []

        for c in regex:
            if c.isalnum():           # a, b, c ...
                output += c
            elif c == "(":
                stack.append(c)
            elif c == ")":
                while stack and stack[-1] != "(":
                    output += stack.pop()
                stack.pop()  # remove "("
            else:
                while stack and stack[-1] != "(" and \
                      self.precedence[c] <= self.precedence[stack[-1]]:
                    output += stack.pop()
                stack.append(c)

        while stack:
            output += stack.pop()

        return output
