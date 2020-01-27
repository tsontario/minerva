import yaml
from os import path
import nltk


class DictBuilder:
    NLTK_STOPWORDS = nltk.corpus.stopwords.words("english")
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
                "UofOCourses.txt",
            )
        )

    # TODO: add optional parameters for enabling/disabling stopwords, stemming/lemmatization, and normalization
    def build(self):
        corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        for doc in corpus_stream:
            self.terms = self.terms.union(self.tokenizer.tokenize(doc.course.contents))

        out = open(self.outfile_path, "w")
        for term in sorted(map(lambda x : x.lower(), self.terms)):
            term = term
            if not term in type(self).NLTK_STOPWORDS:
                out.write(term)
                out.write("\n")
        print(f"{len(self.terms)} unique terms written to {path.abspath(self.outfile_path)}")
