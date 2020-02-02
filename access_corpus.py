from os import path

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor

corpus_path = path.realpath("data/corpus/UofO_Courses.yaml")

ctx = Context(corpus_path, "", "")

print("Initializing CorpusAccessor")
corpus_accessor = CorpusAccessor(ctx)

print("Now accessing docs:")

docs = corpus_accessor.access([587,588,589])

for d in docs:
	print(d)
