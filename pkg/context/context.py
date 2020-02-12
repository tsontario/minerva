import hashlib
from os import path
from .defaults import *


# Context holds the global config settings for the current search engine session
class Context:
    def __init__(
        self,
        corpus_path,
        dict_path,
        inverted_index_path,
        tokenizer=default_tokenizer(),
        enable_casefolding=default_enable_casefolds(),
        enable_stopwords=default_enable_stopwords(),
        enable_stemming=default_enable_stemming(),
        enable_normalization=default_enable_normalization(),
        remove_nonalphanumeric=default_remove_nonalphanumeric(),
    ):
        self._corpus_path = path.abspath(corpus_path)
        self._dict_path = path.abspath(dict_path)
        self._inverted_index_path = path.abspath(inverted_index_path)
        self.tokenizer = tokenizer
        self.enable_casefolding = enable_casefolding
        self.enable_stopwords = enable_stopwords
        self.enable_stemming = enable_stemming
        self.enable_normalization = enable_normalization
        self.remove_nonalphanumeric = remove_nonalphanumeric

    # hacky but works
    def corpus_path(self):
        return self._corpus_path

    def dict_path(self):
        return self._dict_path.strip(".yaml") + f"_{self._digest()}.yaml"

    def inverted_index_path(self):
        return (
            self._inverted_index_path.strip(".yaml") + f"_index_{self._digest()}.yaml"
        )

    def bigram_index_path(self):
        return (
            self._inverted_index_path.strip(".yaml")
            + f"_bigram_index_{self._digest()}.yaml"
        )

    # digest returns the hex digest of the current context object in regards to those elements
    # configurable by the user. This digest can be (indeed, is) appended to the end of generated files
    # such as dictionaries and indices, so that we can maintain persistent records without having
    # to expensively reconstruct these documents every time we change a configuration.
    # NOTE: ideally, the hash would encompass all the possible configurations. However, since we only expose
    # a small subset to the UI, we have chosen to only hash those. Manipulating the configuration at the source
    # is to be done at your own risk.
    def _digest(self):
        to_hash = f"{self.enable_stemming}{self.enable_stopwords}{self.enable_normalization}".encode()
        return hashlib.md5(to_hash).hexdigest()
