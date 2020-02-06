from os import path

from pkg.context import Context
from pkg.editdistance import EditDistance

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
inverted_index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, inverted_index_path)
ed = EditDistance(ctx)

query = "Example Query operoting system lienar"

print(ed.edit_distance(query))
