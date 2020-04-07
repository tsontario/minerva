class TopicLearner:
    # strategy:
    # For each document: take all words (uniq) and use as a VSM query. Then take the top N ranked documents and take their topics.
    # If a topic doesn't exist on the doc.... keep going until you find one.

    # Architecture:
    # static class performs bulk topic assignment
    # We can simply add more topics and rewrite out the corpus with the new values (let's write it to somewhere different, mind you)
    # So... one static method: learn(ctx)
    def __init__(self, ctx, k=5):
        self.ctx = ctx
        self.training_set = []
        self.unclassificed_set = []
        self.k = k

    def learn(self):
        self._load_training_set
        self._load_unclassifed_set
        self._classify
        self._write

    def _load_training_set(self):
        print("STUB")

    def _load_unclassified_set(self):
        print("STUB")

    def _classify(self):
        print("STUB")

    def _write(self):
        print("STUB")
