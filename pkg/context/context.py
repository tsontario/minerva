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
        self.corpus_path = corpus_path
        self.dict_path = dict_path
        self.inverted_index_path = inverted_index_path
        self.tokenizer = tokenizer
        self.enable_casefolding = enable_casefolding
        self.enable_stopwords = enable_stopwords
        self.enable_stemming = enable_stemming
        self.enable_normalization = enable_normalization
        self.remove_nonalphanumeric = remove_nonalphanumeric

    # hacky but works
    def bigram_index_path(self):
        return self.inverted_index_path.strip(".yaml") + "_bigram_index.yaml"
