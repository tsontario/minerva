from yaml import load_all, dump_all

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import string

from itertools import groupby
from .bigram import Bigram


class OttawaUBigramLangModel:
    @staticmethod
    def generate(ctx):
        bigram_lang_models = []
        with open(ctx.corpus_path(), "r") as corpus_handle:
            corpus_stream = load_all(corpus_handle, Loader=Loader)
            for doc in corpus_stream:
                model = OttawaUBigramLangModel._bigram_lang_model_for_doc(doc)
                if len(model.bigrams) == 0:
                    continue
                bigram_lang_models.append(model)
        with open(ctx.bigram_lang_model_path(), "w") as bigram_handle:
            dump_all(
                bigram_lang_models,
                bigram_handle,
                explicit_start=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                Dumper=Dumper,
            )

    @staticmethod
    def _bigram_lang_model_for_doc(doc):
        model_for_doc = OttawaUBigramLangModel(doc.id)
        tokens = doc.read_queryable().split()
        for i, v in enumerate(tokens):
            tokens[i] = v.strip(string.punctuation)  # Remove trailing punctuation
        tokens = [t for t in tokens if t]
        zipped_body = zip(
            tokens[:], tokens[1:]
        )  # sorting is necessary for groupby to work, below
        sorted_bigrams = list(
            zipped_body
        )  # No clue why we need to break this apart so many lines :(
        sorted_bigrams.sort()
        # Get all bigrams, group same bigrams together and count.
        bigram_groups_filtered = filter(
            lambda x: len(x) > 1, [list(g) for k, g in groupby(sorted_bigrams)]
        )
        bigram_groups_list = list(bigram_groups_filtered)
        for bigram_group in bigram_groups_list:
            model_for_doc.add_bigram(Bigram(bigram_group[0], len(bigram_group)))
        return model_for_doc

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.bigrams = []

    def add_bigram(self, bigram):
        self.bigrams.append(bigram)
