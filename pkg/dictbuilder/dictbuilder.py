import yaml
from os import path
import nltk


class DictBuilder:
    BASE_STOPWORDS = nltk.corpus.stopwords.words("english")

    def __init__(
        self, corpus_handle, tokenizer=nltk.TweetTokenizer(), enable_stopwords=False
    ):
        self.tokenizer = tokenizer
        self.corpus_handle = corpus_handle
        self.terms = set()
        self.enable_stopwords = enable_stopwords
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

    def build(self):
        corpus_stream = yaml.load_all(self.corpus_handle, Loader=yaml.Loader)
        for doc in corpus_stream:
            self.terms = self.terms.union(self.tokenizer.tokenize(doc.course.contents))

        out = open(self.outfile_path, "w")

        rejected_terms = []
        for term in sorted(map(lambda x: x.lower(), self.terms)):
            if not self.enable_stopwords or not term in type(self).BASE_STOPWORDS:
                out.write(term)
                out.write("\n")
            else:
                rejected_terms.append(term)

        if len(rejected_terms) > 0:
            print(
                "***The following terms were rejected from the dictionary since they have been identified as STOPWORDS***"
            )
            print(
                "--------------------------------------------------------------------------------------------------------"
            )
            for term in sorted(set(rejected_terms)):
                print(term)
        print(
            f"{len(self.terms) - len(rejected_terms)} unique terms written to {path.abspath(self.outfile_path)}"
        )
