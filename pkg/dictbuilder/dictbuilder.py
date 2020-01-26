import yaml
from os import path
import nltk


class DictBuilder:
    def __init__(self, corpus_handle, tokenizer=nltk.TweetTokenizer()):
        self.tokenizer = tokenizer
        self.corpus_handle = corpus_handle
        self.terms = set()
        self.outfile_path = path.relpath(
            path.join(
                path.realpath(__file__),
                "..",
                "..",
                "..",
                "data",
                "dictionary",
                "UofOCourse.txt",
            )
        )

    # TODO: add optional parameters for enabling/disabling stopwords, stemming/lemmatization, and normalization
    def build(self):
        corpus_stream = yaml.load_all(self.corpus_handle)
        for doc in corpus_stream:
            self.terms = self.terms.union(self.tokenizer.tokenize(doc.course.contents))

        out = open(self.outfile_path, "w")
        for term in sorted(self.terms):
            out.write(term)
            out.write("\n")
        print(len(self.terms))
