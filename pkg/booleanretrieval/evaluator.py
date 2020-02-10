import re

from .util import *
from ..indexaccess import IndexAccessor
from ..indexbuilder import IndexValue
from ..util import Stack

# Evaluator objects evaluate postfix boolean expressions and return the document IDs associated with the
# evaluated expression. The validity of the boolean expression is implicitly assumed and behaviour in violation
# of this precondition is undefined.
class Evaluator:
    def __init__(self, ctx, expr):
        self.ctx = ctx
        self.expr = expr
        self.index_accessor = IndexAccessor(ctx)

    # evaluate first converts each operand into the associated matching document ids.
    # It then evaluates the expression using set-based semantics (eg. AND = intersection, OR = union, etc.).
    # The return value is an array of matching document ids that satisfy the search expression.
    def evaluate(self):
        converted_expr = self._convert_to_doc_ids(self.expr)
        result = self._evaluate(converted_expr)
        return result

    # converts the operands of self.expr into arrays of doc ids
    def _convert_to_doc_ids(self, expr):
        result = []
        for token in expr:
            if is_operator(token):
                result.append(token)
            else:
                indexed_val = self.index_accessor.access(self.ctx, token)
                result.append(set(indexed_val.doc_ids))
        return result

    # Reduces expr down to a single value.
    # If the input expression is well-formed, this routine is guaranteed to result in
    # a single value (a set of document ids). Since we only have binary operators, there can be only N-1 operators (N = number of operands).
    # Every operator evaluation reduces the number of operands by 1. So after evaluating N-1 operators, we have
    # removed N-1 operands -> N - (N-1) = 1 operand left, which is the final result
    def _evaluate(self, expr):
        eval_stack = Stack()
        for token in expr:
            if is_operand(token):
                eval_stack.push(token)
            else:  # must be an operator
                self._do_op(token, eval_stack)
        return eval_stack.pop()

    def _do_op(self, op, stack):
        if op == "AND":
            stack.push(stack.pop() & stack.pop())
        elif op == "OR":
            stack.push(stack.pop() | stack.pop())
        elif op == "AND_NOT":
            # Order is important here, otherwise we take the wrong difference
            target = stack.pop()
            source = stack.pop()
            stack.push(source.difference(target))
