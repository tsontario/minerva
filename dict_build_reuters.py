from os import path

from pkg.dictionary import DictBuilder
from pkg.context import Context

corpus_path = path.realpath("data/corpus/reuters.yaml")
dict_path = path.realpath("data/dictionary/reuters.txt")
# corpus_handle = open("./test.yaml", "r")

ctx = Context(corpus_path, dict_path, "")
dict_builder = DictBuilder(ctx)
dict_builder.build()
