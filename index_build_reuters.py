from os import path

from pkg.index import ReutersIndexBuilder, IndexAccessor
from pkg.context import Context

corpus_path = "data/corpus/reuters.yaml"
dictionary_path = "data/dictionary/reuters.txt"
index_path = path.realpath("data/index/reuters.yaml")

ctx = Context(corpus_path, dictionary_path, index_path)

index_builder = ReutersIndexBuilder(ctx)
index_builder.build()
