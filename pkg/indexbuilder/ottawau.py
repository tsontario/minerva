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

# TODO: So here's what we need to do:
# STEP 1:
#   - FOR EACH DOCUMENT, read the doc, call normalizers/filters, etc. and then generate a TERM -> DOC_ID mapping. DOC_ID should ALSO HAVE NUMBER OF TIMES TERM OCCURS
#   - Once this is done for all documents, alphabetize the list on TERM: identical terms are now together
#   - For a given term: WHILE the current term consider is equal, increase DOC_FREQ by 1 and maintain a list of the DOC_ID (objects!) that make up the list for the terms
#   - The result of these operations is your inverted index. Congratulations

        # corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        # if os.getenv("DEBUG"):
        #     print("Building inverted index (uOttawa)...")
        # doc_level_indices = list()
        # for doc in corpus_stream:
        #     simple_index = InvertedIndexSimple()
        #     contents = doc.read_queryable()
