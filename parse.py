from os import path

from pkg.booleanretrieval import Parser, Evaluator
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")
ctx = Context(corpus_path, dictionary_path, index_path)

parser = Parser(ctx)
parsed = parser.parse("a*bi*")
doc_ids = Evaluator(ctx, parsed).evaluate()

print(doc_ids)
