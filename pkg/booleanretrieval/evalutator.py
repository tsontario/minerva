# Evaluator objects evaluate boolean expressions and return the document IDs associated with the
# evaluated expression
class Evaluator:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        self._convert_to_doc_ids

    # converts the operands of self.expr into arrays of doc ids
    def _convert_to_doc_ids(self):
        for i, token in enumerate(self.expr):
            if is_operand(token):
                pass
