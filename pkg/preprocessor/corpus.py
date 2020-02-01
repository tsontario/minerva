from abc import ABC


# All Corpus objects must implement a `read_queryable` method that is used by downstream modules to parse only those parts of a given document that are
# necessary for a search operation. This allows us to keep metadata about document objects while simplifying the ability of our searh engine to target
# only those fields that are relevant to its use-case.
class Queryable(ABC):
    def read_queryable(self):
        pass
