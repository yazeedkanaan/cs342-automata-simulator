class RegexParser:
    precedence = {
        "*": 3,
        ".": 2,
        "|": 1
    }

    def add_concat(self, regex):
        result = ""
        for i in range(len(regex)):
            result += regex[i]
            if i + 1 < len(regex):
                if regex[i] not in "(|" and regex[i+1] not in "*)|":
                    result += "."
        return result

    def to_postfix(self, regex):
        regex = self.add_concat(regex)
        output = ""
        stack = []

        for c in regex:
            if c.isalnum():
                output += c
            elif c == "(":
                stack.append(c)
            elif c == ")":
                while stack and stack[-1] != "(":
                    output += stack.pop()
                stack.pop()
            else:
                while stack and stack[-1] != "(" and self.precedence[c] <= self.precedence[stack[-1]]:
                    output += stack.pop()
                stack.append(c)

        while stack:
            output += stack.pop()

        return output
