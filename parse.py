from os import path

from pkg.booleanretrieval import Parser, Evaluator
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")
ctx = Context(corpus_path, dictionary_path, index_path)

p = Parser(ctx)
parsed = p.parse("(learn AND (leading OR particular) ) OR material")
doc_ids = Evaluator(ctx, parsed).evaluate()
print(doc_ids)
