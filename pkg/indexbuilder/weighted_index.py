import yaml
from collections import defaultdict
import pkg.indexaccess as indexaccess

# create an weighted_index based on the current index which includes the tf*idf weight
class WeightedIndexBuilder:
    def __init__(self, ctx):
        self.ctx = ctx

    def build(self):
        index = defaultdict(lambda: [])
        # build weighted index ...
        # so for each term in index, we already know the document frequency, but we have to calculate the number of times a term occurs in each document it appears in

        # ie:           in doc 5 once, in doc 8 thrice
        # "science" --> [(5, 1), (8, 3)]



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


