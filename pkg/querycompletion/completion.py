# Final Module 2
# Query Completion Module

from pkg.bigram_lang_model import OttawaUBigramLangModel
from pkg.querycompletion import BigramAccessor
from pkg.context import Context

class Completion:
    def __init__(self, ctx):
        self.ctx = ctx
        self.bigram_accessor = BigramAccessor(self.ctx)

    def complete(self, term):
        completions = []
        for comp in self.bigram_accessor.access(self.ctx, term):
            completions.append(comp.token) # don't need the probabilities
        return completions
