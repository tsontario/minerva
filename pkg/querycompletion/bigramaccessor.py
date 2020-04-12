from yaml import load_all

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from os import path

import pkg.bigram_lang_model.ottawau as ottawau
import pkg.bigram_lang_model.reuters as reuters


class BigramAccessor:
    bigram_models = {}

    # private singleton class
    class __BigramAccessor:
        def __init__(self, ctx):
            self.ctx = ctx
            self.bigrams = {}
            if not path.exists(ctx.bigram_lang_model_path()):
                self._build()

            with open(self.ctx.bigram_lang_model_path(), "r") as bigram_handle:
                bigram_stream = load_all(bigram_handle, Loader=Loader)
                for bi in bigram_stream:
                    self.bigrams[bi[0]] = bi[1]

        def _build(self):
            if self.ctx.corpus_type() is "reuters":
                reuters.ReutersBigramLangModel.generate(self.ctx)
            else:
                ottawau.OttawaUBigramLangModel.generate(self.ctx)

    def __init__(self, ctx):
        if ctx.bigram_lang_model_path() not in self.bigram_models:
            BigramAccessor.bigram_models[
                ctx.bigram_lang_model_path()
            ] = BigramAccessor.__BigramAccessor(ctx)

    def access(self, ctx, term):
        accessor = BigramAccessor.bigram_models[ctx.bigram_lang_model_path()].bigrams
        try:
            return accessor[term]
        except KeyError:
            return []

