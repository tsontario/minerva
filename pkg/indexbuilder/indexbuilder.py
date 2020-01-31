import yaml
import re
import os
from os import path
import nltk


class IndexBuilder:
    def __init__(
        self, corpus_handle, outfile_path, dictionary, tokenizer=nltk.WordPunctTokenizer
    ):
        self.infile = corpus_handle
        self.outfile_path = outfile_path
        self.dictionary = dictionary
        self.tokenizer = tokenizer
