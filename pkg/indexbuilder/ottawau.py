import yaml
import re
import os
from os import path
from collections import defaultdict

import nltk
from .indexbuilder import IndexBuilder
from .invertedindex import IndexValue
from ..dictionary import Dictionary, DictBuilder
from ..wordmodifiers import context


class OttawaUIndexBuilder(IndexBuilder):
    def __init__(self, ctx):
        self.corpus_path = ctx.corpus_path
        self.dict_path = ctx.dict_path
        self.inverted_index_path = ctx.inverted_index_path
        self.tokenizer = ctx.tokenizer
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    def build(self):
        term_documents_dict = self._build_simple_index()

        inverted_index = {}
        for key in term_documents_dict:
            doc_ids = term_documents_dict[key]
            inverted_index[key] = IndexValue(len(doc_ids), doc_ids)

        with open(self.inverted_index_path, "w") as index_file:
            yaml.dump(
                inverted_index,
                index_file,
                explicit_start=True,
                default_flow_style=True,
                sort_keys=False,
                indent=2,
            )

    def _build_simple_index(self):
        simple_index = defaultdict(
            lambda: []
        )  # SOURCE: https://www.accelebrate.com/blog/using-defaultdict-python
        dictionary = Dictionary(self.dict_path)
        with open(self.corpus_path, "r") as corpus_handle:
            corpus = yaml.load_all(corpus_handle, Loader=yaml.Loader)
            for document in corpus:
                # apply normalizations...
                contents = document.read_queryable()
                for normalize_func in self.normalize_funcs:
                    contents = normalize_func(contents)
                terms = self.tokenizer.tokenize(contents)
                # apply filters...
                for filter_func in self.filter_funcs:
                    terms = filter_func(terms.copy())
                for term in terms:
                    if dictionary.contains(term):
                        simple_index[term].append(document.id)
        return simple_index
