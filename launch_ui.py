from os import path
import nltk
print("Ensuring nltk libraries exist...")
nltk.download("stopwords")
nltk.download('wordnet')
from pkg.userinterface import userinterface as ui
from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor
from pkg.dictionary import Dictionary
from pkg.index import IndexAccessor, BigramIndexAccessor, WeightedIndexAccessor



print("Loading default context...")
corpus_path = "data/corpus/UofO_Courses.yaml"
dictionary_path = "data/dictionary/UofOCourses.txt"
index_path = path.realpath("data/index/UofO_Courses.yaml")

ctx = Context(corpus_path, dictionary_path, index_path)

# We do this to eager load our singleton classes into memory to speed up execution during actual search queries
print("Loading corpus...")
corpus = CorpusAccessor(ctx)
print("Loading dictionary")
dictionary = Dictionary(ctx)
print("Loading indices...")
index = IndexAccessor(ctx)
bigram_index = BigramIndexAccessor(ctx)
weighted_index = WeightedIndexAccessor(ctx)
print("Done!")
print("Launch User Interface")
ui.launch()
print("Goodbye!")
