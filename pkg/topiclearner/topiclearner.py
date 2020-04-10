from yaml import load_all, dump_all

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import time
from itertools import chain
from collections import Counter

from ..vsm import VectorSpaceModel
from pkg.corpusaccess import CorpusAccessor


class TopicLearner:
    # strategy:
    # For each document: take all words (uniq) and use as a VSM query. Then take the top N ranked documents and take their topics.
    # If a topic doesn't exist on the doc.... keep going until you find one.

    # Architecture:
    # We can simply add more topics and rewrite out the corpus with the new values (let's write it to somewhere different, mind you)
    # So... one static method: learn(ctx)
    def __init__(self, ctx, k=5):
        self.ctx = ctx
        self.corpus_accessor = CorpusAccessor(ctx)
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

    # Using the training set, classify documents with missing topics
    def _classify(self):
        print("loading VSM")
        start = time.time()
        vsm = VectorSpaceModel(self.ctx)
        end = time.time()
        print(f"loading VSM took {end - start} seconds")
        for article in self.unclassified_set:
            start = time.time()
            results = vsm.search(self.ctx, article.read_queryable())
            documents = self.corpus_accessor.access(self.ctx, [r[0] for r in results])
            documents = [d for d in documents if len(d.topics) > 0]
            documents = documents[: min(5, len(documents))]
            if len(documents) == 0:
                print(
                    f"No possible topic neighbours for {article.title}, skipping assignment"
                )
                continue
            self._assign_topics(article, documents)
            print(f"New topics for {article.title}: {article.topics}")
            end = time.time()
            print(f"Time elapsed for {article.title}: {end - start} seconds")
        full_set = self.unclassified_set + self.training_set
        with open(self.ctx.corpus_path(), "w") as outfile:
            dump_all(
                full_set,
                outfile,
                explicit_start=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                Dumper=Dumper,
            )

    def _write(self):
        print("STUB")

    # Given a set of documents that are the nearest neightbours of article, extract the relevant topics
    # Strategy: from N nearest negihbours, assign topics that appear in the majority
    def _assign_topics(self, article, documents):
        topics = chain.from_iterable([list(d.topics) for d in documents])
        topics_with_occurrences = Counter(topics)
        article.topics = [
            k for (k, val) in topics_with_occurrences.items() if val > self.k / 2
        ]  # majority
        if len(article.topics) == 0:
            # If no clear majority topics, just take the most common topic(s)
            print(f"No majority topics from {topics_with_occurrences}")
            most_common = max(topics_with_occurrences.values())
            article.topics = [
                k for (k, val) in topics_with_occurrences.items() if val == most_common
            ]


def filter_empty(l):
    if len(l) == 0:
        return False