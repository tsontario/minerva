import yaml
from collections import defaultdict
import pkg.indexaccess as indexaccess

# BigramIndexBuilder iterates over all keys of the currently configured index and generates
# a secondary index, which maps each bigram to the terms in the primary index containing
# that bigram.
class BigramIndexBuilder:
    def __init__(self, ctx):
        self.ctx = ctx

    def build(self):
        index = defaultdict(default_index_value)

        # This is a hacky way to get access to all the keys in a given index
        # In general, we only expose 'get' access to a single key at a time, not the full set of keys.
        # If we have time, we can refactor into something nicer but at the end of the day
        # it's just going to be doing this so I'm not too worried.
        index_accessor = indexaccess.IndexAccessor(self.ctx)
        keys = index_accessor.index[self.ctx.inverted_index_path].index.keys()

        for key in keys:
            k = f"${key}$"  # add begin/end indicators
            # SOURCE: https://stackoverflow.com/questions/21303224/iterate-over-all-pairs-of-consecutive-items-in-a-list
            for first, second in zip(k, k[1:]):
                index[first + second].append(key)
        with open(self.ctx.bigram_index_path(), "w") as bigram_handle:
            yaml.dump(
                index,
                bigram_handle,
                explicit_start=True,
                default_flow_style=True,
                sort_keys=False,
                indent=2,
            )


def default_index_value():
    return []
