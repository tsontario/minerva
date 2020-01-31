import os
import re


class CaseFolder:
    def call(self, terms):
        return set(map(lambda term: term.lower(), terms))


class StopWordFilter:
    def __init__(self, stopwords):
        self.stopwords = stopwords

    def call(self, terms):
        rejected_terms = set()
        for term in terms:
            if term in self.stopwords:
                rejected_terms.add(term)
        terms = terms - rejected_terms
        pretty_print_debug_filter_summary("STOPWORDS", rejected_terms)
        return terms


class AlphaNumericFilter:
    def call(self, terms):
        rejected_terms = set()
        pattern = r"^\W+$"  # Matches any non-alphanumeric string
        for term in terms:
            if re.match(pattern, term):
                rejected_terms.add(term)
        terms = terms - rejected_terms
        pretty_print_debug_filter_summary("NONALPHANUMERIC", rejected_terms)
        return terms


class Stemmer:
    def __init__(self, stemmer):
        self.stemmer = stemmer

    def call(self, terms):
        stemmed_terms = set()
        for term in terms:
            stemmed_terms.add(self.stemmer.stem(term))
        if os.getenv("DEBUG"):
            print(
                f"Stemming procedure reduced number of terms from {len(terms)} to {len(stemmed_terms)} (difference = {len(terms) - len(stemmed_terms)})"
            )
        return stemmed_terms


def pretty_print_debug_filter_summary(filter_kind, rejected_terms):
    if len(rejected_terms) > 0 and os.getenv("DEBUG"):
        print(
            f"***The following terms (N={len(rejected_terms)}) were rejected from the dictionary since they have been identified as {filter_kind}***"
        )
        print(
            "--------------------------------------------------------------------------------------------------------------------------------------"
        )
        for term in sorted(set(rejected_terms)):
            print(term)
