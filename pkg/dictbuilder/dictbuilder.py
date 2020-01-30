import yaml
import re
import os
from os import path
import nltk
from nltk.stem import LancasterStemmer


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
            self.normalize_funcs.append(self._normalize_periods)
            self.normalize_funcs.append(self._normalize_hyphens)

        # filter functions should be strictly functional/idempotent and take as parameters only (self, set)
        self.filter_funcs = []
        if enable_casefolding:
            self.filter_funcs.append(self._casefold)
        if enable_stopwords:
            self.filter_funcs.append(self._filter_stopwords)
        if remove_nonalphanumeric:
            self.filter_funcs.append(self._filter_nonalphanumeric)
        if enable_stemming:
            self.filter_funcs.append(self._stem_words)

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

    def _normalize_periods(self, text):
        # SOURCE: https://stackoverflow.com/questions/53149396/regex-to-extract-acronyms
        pattern = r"\b[A-Z](?:[\.&]?[A-Z]){1,7}\b"
        normalized_text = re.sub(pattern, lambda x: re.sub("\.", "", x.group()), text)
        return normalized_text

    def _normalize_hyphens(self, text):
        pattern = r"\b(\w+-)+\w+\b"
        normalized_text = re.sub(pattern, lambda x: re.sub("-", " ", x.group()), text)
        return normalized_text

    def _casefold(self, terms):
        return set(map(lambda x: x.lower(), terms))

    def _filter_stopwords(self, terms):
        rejected_terms = set()
        for term in terms:
            if term in DictBuilder.BASE_STOPWORDS:
                rejected_terms.add(term)
        terms = terms - rejected_terms
        self._pretty_print_debug_filter_summary("STOPWORDS", rejected_terms)
        return terms

    def _filter_nonalphanumeric(self, terms):
        rejected_terms = set()
        pattern = r"^\W+$"  # Matches any non-alphanumeric string
        for term in terms:
            if re.match(pattern, term):
                rejected_terms.add(term)
        terms = terms - rejected_terms
        self._pretty_print_debug_filter_summary("NONALPHANUMERIC", rejected_terms)
        return terms

    def _stem_words(self, terms):
        stemmed_terms = set()
        stemmer = LancasterStemmer()
        for term in terms:
            stemmed_terms.add(stemmer.stem(term))
        if os.getenv("DEBUG"):
            print(
                f"Stemming procedure reduced number of terms from {len(terms)} to {len(stemmed_terms)} (difference = {len(terms) - len(stemmed_terms)})"
            )
        return stemmed_terms

    def _pretty_print_debug_filter_summary(self, filter_kind, rejected_terms):
        if len(rejected_terms) > 0 and os.getenv("DEBUG"):
            print(
                f"***The following terms (N={len(rejected_terms)}) were rejected from the dictionary since they have been identified as {filter_kind}***"
            )
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------"
            )
            for term in sorted(set(rejected_terms)):
                print(term)
