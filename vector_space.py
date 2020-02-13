from os import path
from pkg.vsm import VectorSpaceModel

from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
inverted_index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, inverted_index_path)

print("Initializing VSM")
vector_model = VectorSpaceModel(ctx)

print(vector_model.search(ctx, "linear algebra"))