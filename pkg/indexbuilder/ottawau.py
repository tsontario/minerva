import yaml
import re
import os
from os import path
import nltk


class OttawaUIndexBuilder(IndexBuilder):
    def __init__(
        self, corpus_handle, outfile_path, dictionary, tokenizer=nltk.WordPunctTokenizer
    ):
        self.infile = corpus_handle
        self.outfile_path = outfile_path
        self.dictionary = dictionary
        self.tokenizer = tokenizer

    def build(self):
        corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        if os.getenv("DEBUG"):
            print("Building inverted index (uOttawa)...")
        for doc in corpus_stream:
            contents = doc.read_queryable()
            
