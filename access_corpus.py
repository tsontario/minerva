from os import path

from pkg.context import Context
from pkg.corpusaccess import CorpusAccessor

corpus_path = path.realpath("data/corpus/UofO_Courses.yaml")

ctx = Context(corpus_path, "", "")

print("Initializing CorpusAccessor")
corpus_accessor = CorpusAccessor(ctx)

print("Getting size??")
print(corpus_accessor.get_size())


# print("Accessing docs:")

# docs = corpus_accessor.access(ctx, [587, 588, 589])

# for d in docs:
#     print(d)

# print("\nTry initializing again with same corpus (doesn't re-load)")
# corpus_accessor = CorpusAccessor(ctx)

# print("Accessing docs:")

# docs = corpus_accessor.access(ctx, [590, 591, 592])

# for d in docs:
#     print(d)
