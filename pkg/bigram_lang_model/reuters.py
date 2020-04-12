from yaml import load_all, dump_all

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import string
from collections import defaultdict

from itertools import groupby
from .bigram import Bigram


class ReutersBigramLangModel:
    @staticmethod
    def generate(ctx):
        bigrams = defaultdict(int) # so that bigrams have count 0 to begin with
        frequencies = defaultdict(int)
        with open(ctx.corpus_path(), "r") as corpus_handle:
            corpus_stream = load_all(corpus_handle, Loader=Loader)
            for doc in corpus_stream:
                body_tokens = doc.body.split()
                title_tokens = doc.title.split()
                for i, v in enumerate(title_tokens):
                    title_tokens[i] = v.strip(string.punctuation).lower()  # Remove trailing punctuation, convert to same case (so eg. 'The' == 'the')
                for i, v in enumerate(body_tokens):
                    body_tokens[i] = v.strip(string.punctuation).lower()  # Remove trailing punctuation, convert to same case (so eg. 'The' == 'the')
                body_tokens = [t for t in body_tokens if t]
                zipped_body = zip(
                    body_tokens[:], body_tokens[1:]
                )  # sorting is necessary for groupby to work, below
                zipped_title = zip(title_tokens[:], title_tokens[1:])
                sorted_bigrams = list(zipped_body) + list(
                    zipped_title
                )  # No clue why we need to break this apart so many lines :(
                sorted_bigrams.sort()
                # Get all bigrams, group same bigrams together and count.
                bigram_groups_filtered = filter(
                    lambda x: len(x) > 0, [list(g) for k, g in groupby(sorted_bigrams)]
                )
                bigram_groups_list = list(bigram_groups_filtered)
                for bigram_group in bigram_groups_list:
                    bigrams[bigram_group[0]] += len(bigram_group)
                    for term in bigram_group[0]:
                        frequencies[term] += 1
        
        bigram_model = defaultdict(list)
        for tokens, bi_frequency in bigrams.items():
            frequency = bi_frequency/frequencies[tokens[0]]
            bigram_model[tokens[0]].append(Bigram(tokens[1], frequency))   
            # P(w2 | w1) = count(w1, w2) / count(w1)
            # Probability of w2 given w1 = count of bigram (w1,w2) divided by count of w1
            # where w1 comes before w2

        # only save top 3 most probable words (include ties)
        for term, bigrams in bigram_model.items():
            bigram_model[term] = sorted(bigram_model[term], key=lambda x: x.probability, reverse=True)[:3]

        with open(ctx.bigram_lang_model_path(), "w") as bigram_handle:
            dump_all(
                bigram_model.items(),
                bigram_handle,
                explicit_start=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                Dumper=Dumper,
            )
