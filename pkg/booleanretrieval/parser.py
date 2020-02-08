import re

from ..wordmodifiers import context


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
    def __init__(self, ctx):
        self.tokenizer = ctx.tokenizer
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    # Parsing requires multiple steps in order to ensure we are ending up with a query that can
    # be both easily and reliably processed.
    # Step 1: Strip whitespace, ensure enclosing brackets
    # Step 2: Tokenize into parantheses, operators, and operands
    # Step 3: Apply normalizers/filters from execution context settings
    # Step 4: Substitute operands with relevant doc ids
    # Step 5: Evalutate the query (result = array of doc ids)
    def parse(self, expr):
        expr = self._clean(expr)
        expr = self._tokenize(expr)
        expr = self._normalize(expr)
        expr = self._filter(expr)
        print(expr)
        breakpoint()
        postfix_expr = self._to_postfix(expr)
        return postfix_expr

    # Remove extra whitespace, add enclosing parens if needed
    # Code not right, need fix
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

    def _normalize(self, expr):
        result = []
        for e in expr:
            if not is_operand(e):
                result.append(e)
            else:
                for normalize_func in self.normalize_funcs:
                    e = normalize_func(e)
                result.append(e)
        return result

    def _filter(self, expr):
        result = []
        for e in expr:
            if not is_operand(e):
                result.append(e)
            else:
                e = set([e])  # Filter funcs expect sets of words, not simple Strings
                for filter_func in self.filter_funcs:
                    e = filter_func(e)
                if len(e) == 0:
                    e = set([""])  # Stopwords are reduced to empty string
                elif len(e) > 1:
                    raise "Expected filtered/normalized word to be a single element"
                result.append(e.pop())
        return result

    # SOURCE: https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    def _to_postfix(self, expr):
        result = []
        operator_stack = Stack()
        for e in expr:
            if is_operand(e):
                result.append(e)
            elif is_left_parens(e):
                operator_stack.push(e)
            elif is_right_parens(e):
                popped = operator_stack.pop()
                if popped == "(":
                    continue
                result.append(popped)
            elif is_operator(e):
                operator_stack.push(e)
        while True:
            popped = operator_stack.pop()
            if popped is None:
                break
            elif popped == "(":
                continue
            result.append(popped)
        return result


def is_operator(token):
    return token in ["AND", "OR", "NOT"]


def is_operand(token):
    return token not in ["AND", "OR", "NOT", "(", ")"]


def is_left_parens(c):
    return c == "("


def is_right_parens(c):
    return c == ")"


def is_parens(c):
    return is_right_parens(c) or is_left_parens(c)
