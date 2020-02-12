from os import path

from pkg.userinterface import userinterface as ui
from pkg.context import Context
from pkg.dictionary import Dictionary
from pkg.index import IndexAccessor, BigramIndexAccessor


print("Loading default context...")
corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, index_path)

print("Loading files...")
# We do this to eager load our singleton classes into memory to speed up execution during actual search queries
dictionary = Dictionary(ctx)
index = IndexAccessor(ctx)
bigram_index = BigramIndexAccessor(ctx)

print("Launch User Interface")
ui.launch()
print("Goodbye!")
