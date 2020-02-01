import yaml
import re
import os
from os import path
from collections import defaultdict

import nltk
from .indexbuilder import IndexBuilder
from .invertedindex import IndexKey
from ..dictionary import Dictionary, DictBuilder
from ..wordmodifiers import *


class OttawaUIndexBuilder(IndexBuilder):
    def __init__(self, ctx):
        self.corpus_path = ctx.corpus_path
        self.dict_path = ctx.dict_path
        self.inverted_index_path = ctx.inverted_index_path
        self.tokenizer = ctx.tokenizer

        # TODO extract filter func construction to shareable util module that takes as argument a Context object
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
        term_documents_dict = self._build_simple_index()

        inverted_index = {}
        for key in term_documents_dict:
            doc_ids = term_documents_dict[key]
            key_with_freq = IndexKey(key, len(doc_ids))
            inverted_index[key_with_freq] = doc_ids

        with open(self.inverted_index_path, "w") as index_file:
            (
                yaml.dump(
                    inverted_index,
                    index_file,
                    explicit_start=True,
                    default_flow_style=True,
                    sort_keys=False,
                    indent=2,
                )
            )

    def _build_simple_index(self):
        simple_index = {}
        dictionary = Dictionary(self.dict_path)
        with open(self.corpus_path, "r") as corpus_handle:
            corpus = yaml.load_all(corpus_handle, Loader=yaml.Loader)
            for document in corpus:
                # apply normalizations...
                contents = document.read_queryable()
                for normalize_func in self.normalize_funcs:
                    contents = normalize_func(document.read_queryable())
                terms = self.tokenizer.tokenize(contents)
                # apply filters...
                for filter_func in self.filter_funcs:
                    terms = filter_func(terms.copy())
                for term in terms:
                    if dictionary.contains(term):
                        if simple_index.get(term, None) is None:
                            simple_index[term] = [document.id]
                        else:
                            simple_index[term] = simple_index[term] + [document.id]
        return simple_index
