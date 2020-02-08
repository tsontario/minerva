from os import path

<<<<<<< HEAD
from pkg.booleanretrieval import Parser, Evaluator
=======
from pkg.booleanretrieval import parser
>>>>>>> Apply same set of filters/normalizers to query as to current dict/index
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")
ctx = Context(corpus_path, dictionary_path, index_path)

<<<<<<< HEAD
p = Parser(ctx)
parsed = p.parse("(learn AND (leading OR particular) ) OR material")
doc_ids = Evaluator(ctx, parsed).evaluate()
print(doc_ids)
=======
p = parser.Parser(ctx)
p.parse("word OR a AND (another OR alternate)")
>>>>>>> Apply same set of filters/normalizers to query as to current dict/index
