from os import path
from pkg.vsm import VectorSpaceModel

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
inverted_index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, inverted_index_path)

corpus_accessor = CorpusAccessor(ctx)

print("Initializing VSM")
vector_model = VectorSpaceModel(ctx)

query = "health care"
print("VSM results for query: '" + query + "'")

results = vector_model.search(ctx, query)

for r in results:
	doc = corpus_accessor.access(ctx, [r[0]])
	print(str(doc[0]) + " >>> " + "{:.4f}".format(r[1]))
