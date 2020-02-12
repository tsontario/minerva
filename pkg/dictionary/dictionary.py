import yaml
from os import path

from .dictbuilder import DictBuilder

# Dictionary is an in-memory representation of the dictionary of terms for a given corpus
# Internally, we represent the volume as a set, since that gives us O(1) access, which makes
# constructing an index much faster.
class Dictionary:
    # key = dictionary path, value = set of terms
    dictionary = {}

    class __Dictionary:
        def __init__(self, ctx):
            self.ctx = ctx
            self.terms = set()
            if not path.exists(ctx.dict_path()):
                DictBuilder(ctx).build()
            with open(self.ctx.dict_path(), "r") as terms:
                for term in terms:
                    self.terms.add(term.rstrip())  # remove trailing newline

        def add(self, term):
            self.terms.add(term)

        def contains(self, term):
            return term in self.terms

    def __init__(self, ctx):
        self.ctx = ctx
        if ctx.dict_path() not in Dictionary.dictionary:
            Dictionary.dictionary[ctx.dict_path()] = Dictionary.__Dictionary(ctx)
