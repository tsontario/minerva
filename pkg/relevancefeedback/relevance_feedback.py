from collections import defaultdict


class RelevanceFeedback:
    class __RelevanceFeedback:
        def __init__(self, alpha, beta, gamma):
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.relevance = defaultdict(default_index_value)

    relevance = {}

    def __init__(self, alpha=1, beta=0.75, gamma=0.15):
        if not "relevance" in self.relevance:
            RelevanceFeedback.relevance[
                "relevance"
            ] = RelevanceFeedback.__RelevanceFeedback(alpha, beta, gamma)

    def access(self, query):
        return self.relevance["relevance"].relevance[query]

    def set_relevant(self, query, doc):
        for d in self.relevance["relevance"].relevance[query]:
            if d[1] == doc[1]:
                return
        self.relevance["relevance"].relevance[query].append(doc)

    def unset_relevant(self, query, doc):
        to_delete = -1
        for i, d in enumerate(self.relevance["relevance"].relevance[query]):
            if d[1] == doc[1]:
                to_delete = i
        if to_delete != -1:
            del (self.relevance["relevance"].relevance[query], to_delete)


def default_index_value():
    return []
