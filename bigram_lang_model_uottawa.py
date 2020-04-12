from os import path

from pkg.bigram_lang_model import OttawaUBigramLangModel
from pkg.querycompletion import BigramAccessor
from pkg.querycompletion import Completion
from pkg.context import Context

corpus_path = "data/corpus/UofO_Courses.yaml"

ctx = Context(corpus_path, "None", "None")

OttawaUBigramLangModel.generate(ctx)
bi = Completion(ctx).complete("the")

# bigram_accessor = BigramAccessor(ctx)
# bi = bigram_accessor.access(ctx, "the")

for b in bi:
	print(b)