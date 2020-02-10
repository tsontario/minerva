import yaml
from ..indexbuilder import IndexValue


class IndexAccessor:
    index = {}
    bigram_index = {}

    # private 'constructor' for singleton
    # design pattern followed from: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    class __IndexAccessor:
        def __init__(self, ctx):
            self.ctx = ctx
            with open(self.ctx.inverted_index_path, "r") as index_handle:
                self.index = yaml.load(index_handle, Loader=yaml.Loader)

            with open(self.ctx.bigram_index_path(), "r") as bigram_index_handle:
                self.bigram_index = yaml.load(bigram_index_handle, Loader=yaml.Loader)

    def __init__(self, ctx):
        # if the index is not yet in accessor, then opportunistically load the index
        if ctx.inverted_index_path not in self.index:
            IndexAccessor.index[
                ctx.inverted_index_path
            ] = IndexAccessor.__IndexAccessor(ctx)
            # is using the corpus_path as a dict key a bad idea?
        else:
            print("Corpus " + ctx.corpus_path + " already loaded.")

    def access(self, ctx, term):
        accessor = IndexAccessor.index[ctx.inverted_index_path]
        try:
            return accessor.index[term]
        except KeyError:
            return IndexValue(0, [])

    def access_secondary(self, ctx, term):
        accessor = IndexAccessor.index[ctx.inverted_index_path].bigram_index
        try:
            return accessor[term]
        except KeyError:
            return []
