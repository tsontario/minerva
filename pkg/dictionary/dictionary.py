# Dictionary is an in-memory representation of the dictionary of terms for a given corpus
# Internally, we represent the volume as a set, since that gives us O(1) access, which makes
# constructing an index much faster.
class Dictionary:
    def __init__(self, path):
        self.terms = set()
        with open(path) as terms:
            for term in terms:
                self.terms.add(term.rstrip())  # remove trailing newline

    def add(self, term):
        self.terms.add(term)

    def contains(self, term):
        return term in self.terms
