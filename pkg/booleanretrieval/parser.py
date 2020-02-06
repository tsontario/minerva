import re


class Stack:
    def __init__(self):
        self._stack = []

    def push(self, val):
        self._stack.append(val)
        return val

    def pop(self):
        if len(self._stack) == 0:
            return None
        return self._stack.pop()


# Example: (computer AND thing)
class Parser:
    def parse(self, expr):
        expr = self._clean(expr)
        expr = self._tokenize(expr)
        postfix_expr = self._to_postfix(expr)
        return postfix_expr

    # Remove extra whitespace, add enclosing parens if needed
    def _clean(self, expr):
        expr = expr.strip()
        if expr[0] != "(":
            expr = f"({expr})"
        return expr

    def _tokenize(self, expr):
        result = []
        i = 0
        while i < len(expr):
            if is_parens(expr[i]):
                result.append(expr[i])
                i += 1
            elif re.match(r"\s", expr[i]):  # whitespace
                i += 1
            else:  # an operator or operand
                word = ""
                while (
                    i < len(expr) and re.match(r"\s|\(|\)", expr[i]) is None
                ):  # Not whitespace and not a parens
                    word += expr[i]
                    i += 1
                result.append(word)
        return result

    # SOURCE: https://www.includehelp.com/c/infix-to-postfix-conversion-using-stack-with-c-program.aspx
    def _to_postfix(self, expr):
        # Code not right, need fix
        stack = Stack()
        result = []
        for c in expr:
            if is_operator(c):
                while True:
                    popped = stack.pop()
                    if popped is "(":
                        stack.push(popped)
                        break
                    if popped is None:
                        break
                    result.append(popped)
                stack.push(c)
            elif is_left_parens(c):
                stack.push(c)
            elif is_right_parens(c):
                while True:
                    popped = stack.pop()
                    if popped == "(":
                        break
                    result.append(c)
            else:  # This must be an operator
                result.append(c)
        return result


def is_operator(token):
    return token in ["AND", "OR", "NOT"]


def is_left_parens(c):
    return c == "("


def is_right_parens(c):
    return c == ")"


def is_parens(c):
    return is_right_parens(c) or is_left_parens(c)


parser = Parser().parse("   comp AND (Sci   OR feeding)")
breakpoint()
