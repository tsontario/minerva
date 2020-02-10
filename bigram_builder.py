from os import path

from pkg.indexbuilder import BigramIndexBuilder
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, index_path)

BigramIndexBuilder(ctx).build()
