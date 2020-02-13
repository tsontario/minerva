from os import path

from pkg.index import OttawaUIndexBuilder, WeightedIndexAccessor
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, index_path)

OttawaUIndexBuilder(ctx).build_weighted_index()

index_accessor = WeightedIndexAccessor(ctx)

print(index_accessor.access(ctx, "algorithm")[393])