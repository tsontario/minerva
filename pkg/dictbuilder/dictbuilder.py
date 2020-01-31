import yaml
import re
import os
from os import path
import nltk
from nltk.stem import LancasterStemmer
from ..wordmodifiers import *


class DictBuilder:
    BASE_STOPWORDS = nltk.corpus.stopwords.words("english")

    # TODO separate options out into Config class (We will need to pass a lot of similar info to the query processor to synchronzie the query vocab with the dictionary vocab)
    def __init__(
        self,
        corpus_handle,
        tokenizer=nltk.WordPunctTokenizer(),
        enable_casefolding=True,
        enable_stopwords=False,
        enable_stemming=False,
        enable_normalization=False,
        remove_nonalphanumeric=True,
    ):
        self.tokenizer = tokenizer
        self.corpus_handle = corpus_handle
        self.outfile_path = path.relpath(
            path.join(
                path.realpath(__file__),
                "..",
                "..",
                "..",
                "data",
                "dictionary",
                "UofOCourses.txt",
            )
        )

        # normalizing functions must be called directly on the corpus, not the tokenized terms
        # note that normalizing function change the actual text of the corpus, not a generated token (which happens further downstream)
        self.normalize_funcs = []
        if enable_normalization:
            self.normalize_funcs.append(Normalizer.normalize_periods)
            self.normalize_funcs.append(Normalizer.normalize_hyphens)

        # filter functions should be strictly functional/idempotent and take as parameters only (self, set)
        self.filter_funcs = []
        if enable_casefolding:
            self.filter_funcs.append(CaseFolder().call)
        if enable_stopwords:
            self.filter_funcs.append(StopWordFilter(DictBuilder.BASE_STOPWORDS).call)
        if remove_nonalphanumeric:
            self.filter_funcs.append(AlphaNumericFilter().call)
        if enable_stemming:
            self.filter_funcs.append(Stemmer(nltk.LancasterStemmer()).call)

    def build(self):
        terms = set()
        corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        if os.getenv("DEBUG"):
            print("Performing configured normalizations and tokenization...")
        for doc in corpus_stream:
            # apply normalizations...
            for normalize_func in self.normalize_funcs:
                doc.course.contents = normalize_func(doc.course.contents)
            terms = terms.union(self.tokenizer.tokenize(doc.course.contents))

        # apply filters...
        for filter_func in self.filter_funcs:
            terms = filter_func(terms.copy())
        out = open(self.outfile_path, "w")
        for term in sorted(terms):
            out.write(term)
            out.write("\n")
        print(f"{len(terms)} unique terms written to {path.abspath(self.outfile_path)}")
