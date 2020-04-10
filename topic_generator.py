from os import path

from pkg.topiclearner import TopicLearner
from pkg.context import Context

corpus_path = "data/corpus/reuters.yaml"
dictionary_path = "data/dictionary/reuters.txt"
index_path = path.realpath("data/index/reuters.yaml")

ctx = Context(corpus_path, dictionary_path, index_path,
    enable_casefolding=False, enable_stopwords=False,enable_stemming=False,enable_normalization=False, remove_nonalphanumeric=False)

TopicLearner(ctx).learn()
