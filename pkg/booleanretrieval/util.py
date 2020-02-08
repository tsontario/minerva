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
