from os import path

from pkg.bigram_lang_model import OttawaUBigramLangModel
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"

ctx = Context(corpus_path, "None", "None")

OttawaUBigramLangModel.generate(ctx)
