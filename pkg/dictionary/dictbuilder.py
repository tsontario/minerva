import yaml
import re
import os
from os import path
import nltk
from nltk.stem import LancasterStemmer
from ..wordmodifiers import context
from pkg.preprocessor import Document


class DictBuilder:
    def __init__(self, ctx):
        self.ctx = ctx
        self.tokenizer = ctx.tokenizer
        self.corpus_path = ctx.corpus_path
        self.outfile_path = ctx.dict_path
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    def build(self):
        terms = set()
        with open(self.ctx.corpus_path, "r") as corpus_handle:
            corpus_stream = yaml.load_all(corpus_handle, Loader=yaml.Loader)
            if os.getenv("DEBUG"):
                print("Performing configured normalizations and tokenization...")
            for doc in corpus_stream:
                contents = doc.read_queryable()
                for normalize_func in self.normalize_funcs:
                    contents = normalize_func(doc.read_queryable())
                terms = terms.union(self.tokenizer.tokenize(contents))
        for filter_func in self.filter_funcs:
            terms = filter_func(terms.copy())
        with open(self.outfile_path, "w") as outfile:
            for term in sorted(terms):
                outfile.write(term)
                outfile.write("\n")
        print(f"{len(terms)} unique terms written to {path.abspath(self.outfile_path)}")
