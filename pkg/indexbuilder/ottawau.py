import yaml
import re
import os
from os import path
import nltk
from .indexbuilder import IndexBuilder
from .invertedindex import InvertedIndexSimple


class OttawaUIndexBuilder(IndexBuilder):
    def __init__(self, ctx):
        self.corpus_path = ctx.corpus_path
        self.dict_path = ctx.dict_path
        self.inverted_index_path = ctx.inverted_index_path
        self.tokenizer = ctx.tokenizer

    def build(self):
        self.corpus_handle = open(self.corpus_path, 'r')
        self.dict_handle = open(self.dict_path, 'r')
        self.inverted_index_handle = open(self.inverted_index_path, 'w')

        # corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        # if os.getenv("DEBUG"):
        #     print("Building inverted index (uOttawa)...")
        # doc_level_indices = list()
        # for doc in corpus_stream:
        #     simple_index = InvertedIndexSimple()
        #     contents = doc.read_queryable()
