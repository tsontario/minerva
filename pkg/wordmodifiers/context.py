from ..context import Context
from .filters import *
from .normalizers import *
import nltk

BASE_STOPWORDS = nltk.corpus.stopwords.words("english")

# normalizing functions must be called directly on the corpus, not the tokenized terms
# note that normalizing function change the actual text of the corpus, not a generated token (which happens further downstream)
def normalizer_funcs_for_context(ctx):
    normalize_funcs = []
    if ctx.enable_normalization:
        normalize_funcs.append(Normalizer.normalize_periods)
        normalize_funcs.append(Normalizer.normalize_hyphens)
    return normalize_funcs


# filter functions should be strictly functional/idempotent and take as parameters only (self, set)
def filter_funcs_for_context(ctx):
    filter_funcs = []
    if ctx.enable_casefolding:
        filter_funcs.append(CaseFolder().call)
    if ctx.enable_stopwords:
        filter_funcs.append(StopWordFilter(BASE_STOPWORDS).call)
    if ctx.remove_nonalphanumeric:
        filter_funcs.append(AlphaNumericFilter().call)
    if ctx.enable_stemming:
        filter_funcs.append(Stemmer(nltk.LancasterStemmer()).call)
    return filter_funcs
