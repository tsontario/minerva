from os import path

from pkg.bigram_lang_model import ReutersBigramLangModel
from pkg.context import Context

corpus_path = "data/corpus/reuters.yaml"

ctx = Context(corpus_path, "None", "None")

ReutersBigramLangModel.generate(ctx)
