import yaml
from .invertedindex import IndexValue


class BigramIndexAccessor:
    bigram_index = {}

    # private singleton class
    class __BigramIndexAccessor:
        def __init__(self, ctx):
            self.ctx = ctx

            with open(self.ctx.bigram_index_path(), "r") as bigram_index_handle:
                self.bigram_index = yaml.load(bigram_index_handle, Loader=yaml.Loader)

    def __init__(self, ctx):
        if ctx.bigram_index_path() not in self.bigram_index:
            BigramIndexAccessor.bigram_index[
                ctx.bigram_index_path()
            ] = BigramIndexAccessor.__BigramIndexAccessor(ctx)

    def access(self, ctx, term):
        accessor = IndexAccessor.index[ctx.inverted_index_path].bigram_index
        try:
            return accessor[term]
        except KeyError:
            return []


class IndexAccessor:
    index = {}

    # private 'constructor' for singleton
    # design pattern followed from: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    # Note that the caller is responsible for ensuring both indices exist on disk, otherwise this will throw
    # FileNotFoundError
    class __IndexAccessor:
        def __init__(self, ctx):
            self.ctx = ctx
            with open(self.ctx.inverted_index_path, "r") as index_handle:
                self.index = yaml.load(index_handle, Loader=yaml.Loader)

    def __init__(self, ctx):
        # if the index is not yet in accessor, then opportunistically load the index
        if ctx.inverted_index_path not in self.index:
            IndexAccessor.index[
                ctx.inverted_index_path
            ] = IndexAccessor.__IndexAccessor(ctx)
            # is using the corpus_path as a dict key a bad idea?

    def access(self, ctx, term):
        accessor = IndexAccessor.index[ctx.inverted_index_path]
        try:
            return accessor.index[term]
        except KeyError:
            return IndexValue(0, [])
