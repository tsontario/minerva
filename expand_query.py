from os import path

from pkg.context import Context
from pkg.queryexpansion import Expansion

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
inverted_index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, inverted_index_path)
exp = Expansion(ctx)

q = "coffee stock oil dog cat algebra"
query = exp.expand(q)

for term in query.items():
	print(term)
