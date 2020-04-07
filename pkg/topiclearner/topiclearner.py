from yaml import load_all, dump_all

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from ..vsm import VectorSpaceModel


class TopicLearner:
    # strategy:
    # For each document: take all words (uniq) and use as a VSM query. Then take the top N ranked documents and take their topics.
    # If a topic doesn't exist on the doc.... keep going until you find one.

    # Architecture:
    # We can simply add more topics and rewrite out the corpus with the new values (let's write it to somewhere different, mind you)
    # So... one static method: learn(ctx)
    def __init__(self, ctx, k=5):
        self.ctx = ctx
        self.training_set = []
        self.unclassified_set = []
        self.k = k

    def learn(self):
        self._partition_articles()
        self._classify()
        self._write()

    # partition documents between those that have topics (TRAINING SET) and those that don't
    def _partition_articles(self):
        with open(self.ctx.corpus_path(), "r") as corpus_handle:
            corpus_stream = load_all(corpus_handle, Loader=Loader)
            for article in corpus_stream:
                if len(article.topics) > 0:
                    self.training_set.append(article)
                else:
                    self.unclassified_set.append(article)
        print(
            f"Size of training set: {len(self.training_set)}\nSize of articles to categorize: {len(self.unclassified_set)}"
        )

    def _classify(self):
        print("loading VSM")
        vsm = VectorSpaceModel(self.ctx)
        # for article in self.unclassified_set:
        print(vsm.search(self.ctx, self.unclassified_set[0].read_queryable()))

    def _write(self):
        print("STUB")
