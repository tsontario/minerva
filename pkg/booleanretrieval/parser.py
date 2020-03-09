import re

from ..index import BigramIndexAccessor
from ..wordmodifiers import context
from ..util import Stack
from .util import *

# Parser exposes a single public method, parse, that will convert the provided infix boolean expression
# into a tokenized postfix expression. Its constructor takes a context.Context object to ensure it is
# parameterized the same way as upstream entities (e.g. the index)
class Parser:
    def __init__(self, ctx):
        self.ctx = ctx
        self.index_accessor = BigramIndexAccessor(ctx)
        self.tokenizer = ctx.tokenizer
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    # Parsing transforms the provided boolean expression in the following ways:
    # Step 1: Strip whitespace, ensure enclosing brackets are present
    # Step 2: Tokenize into parantheses, operators, and operands
    # Step 3: Apply normalizers/filters from execution context settings
    # Step 4: Transform into postfix expression for further evaluation
    def parse(self, expr):
        expr = self._clean(expr)
        expr = self._tokenize(expr)
        expr = self._normalize(expr)
        expr = self._filter(expr)
        expr = self._expand_wildcards(expr)
        postfix_expr = self._to_postfix(expr)
        return postfix_expr

    # Remove extra whitespace, add enclosing parens if needed
    # Code not right, need fix
    def _clean(self, expr):
        return expr.strip()

    # Convert an expression into tokens (e.g. (foo AND bar) becomes ["(", "foo", "AND", "bar", ")"])
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

    # Apply any applicable normalizations. This is done to bring query terms into alignment with index entries
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

    # Apply any applicable filters to the input. This is done to bring query terms into alignment with index entries
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

    # expand_wildcards iterates over every token in expr and, if a wildcard is present,
    # expands it using a secondary bigram index on the primary index of dictionary terms.
    # We take the following approach:
    # If the token contains no wildcard, do nothing
    # If the token contains wildcard(s), partition the string, separating along "*"s
    # Find all bigram matches and return the set of dictionary terms
    # Postfilter using a naive regex against the returned set
    def _expand_wildcards(self, expr):
        result = []
        for token in expr:
            if "*" not in token:
                result.append(token)
                continue
            with_boundary = f"${token}$"
            partitioned = with_boundary.split("*")
            partial_result = []
            prepend_or = False
            for partition in partitioned:
                terms = set()
                for first, second in zip(partition, partition[1:]):
                    pair = first + second
                    terms |= set(self.index_accessor.access(self.ctx, pair))
                # We expect no special chars in the input so we can take the naive regex from the wildcarded token directly
                # e.g `foo*bar` becomes `^foo.*bar$`. Note that escape characters inside the search query may negatively impact this unless
                # we explicitly escape them (TODO:)
                regex_formatted_wildcard = re.sub(r"\*", ".*", token)
                postfilter_pattern = re.compile(f"^{regex_formatted_wildcard}$")
                for term in terms:
                    if re.match(postfilter_pattern, term):
                        partial_result.append(term)
                # For every partition except the first, ensure we have an appended OR to the expression
                if not prepend_or:
                    # Convert [term1, term2, tern3, ...] to "term1 OR term2 OR term3... OR termX"
                    result.extend("(")
                    result.extend(" OR ".join(partial_result).split(" "))
                    prepend_or = True
                else:
                    result.extend(["OR"])
                    result.extend(" OR ".join(partial_result).split(" "))
            result.extend(")")
        return result

    # Convert the provided infix expression into postfix. Assumes the provided input is valid
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
                while True:
                    popped = operator_stack.pop()
                    if popped == "(":
                        break
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
