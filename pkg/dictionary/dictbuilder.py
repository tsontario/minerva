import yaml
import re
import os
from os import path
import nltk
from nltk.stem import LancasterStemmer
from ..wordmodifiers import *
from pkg.preprocessor import Document


class DictBuilder:
    BASE_STOPWORDS = nltk.corpus.stopwords.words("english")

    # TODO separate options out into Config class (We will need to pass a lot of similar info to the query processor to synchronzie the query vocab with the dictionary vocab)
    def __init__(self, ctx):
        self.ctx = ctx
        self.tokenizer = ctx.tokenizer
        self.corpus_path = ctx.corpus_path
        self.outfile_path = ctx.dict_path

        # normalizing functions must be called directly on the corpus, not the tokenized terms
        # note that normalizing function change the actual text of the corpus, not a generated token (which happens further downstream)
        self.normalize_funcs = []
        if ctx.enable_normalization:
            self.normalize_funcs.append(Normalizer.normalize_periods)
            self.normalize_funcs.append(Normalizer.normalize_hyphens)

        # filter functions should be strictly functional/idempotent and take as parameters only (self, set)
        self.filter_funcs = []
        if ctx.enable_casefolding:
            self.filter_funcs.append(CaseFolder().call)
        if ctx.enable_stopwords:
            self.filter_funcs.append(StopWordFilter(DictBuilder.BASE_STOPWORDS).call)
        if ctx.remove_nonalphanumeric:
            self.filter_funcs.append(AlphaNumericFilter().call)
        if ctx.enable_stemming:
            self.filter_funcs.append(Stemmer(nltk.LancasterStemmer()).call)

    def build(self):
        terms = set()
        with open(self.ctx.corpus_path, "r") as corpus_handle:
            corpus_stream = yaml.load_all(corpus_handle, Loader=yaml.Loader)
            if os.getenv("DEBUG"):
                print("Performing configured normalizations and tokenization...")
            for doc in corpus_stream:
                # apply normalizations...
                contents = doc.read_queryable()
                for normalize_func in self.normalize_funcs:
                    contents = normalize_func(doc.read_queryable())
                terms = terms.union(self.tokenizer.tokenize(contents))

        # apply filters...
        for filter_func in self.filter_funcs:
            terms = filter_func(terms.copy())
        with open(self.outfile_path, "w") as outfile:
            for term in sorted(terms):
                outfile.write(term)
                outfile.write("\n")
        print(f"{len(terms)} unique terms written to {path.abspath(self.outfile_path)}")
