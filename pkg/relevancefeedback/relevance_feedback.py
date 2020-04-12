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
            RelevanceFeedback.relevance["relevance"] = RelevanceFeedback.__RelevanceFeedback(alpha, beta, gamma)
    
    def access(self, query):
        return self.relevance['relevance'].relevance[query]

    def set_relevant(self, query, doc_id):
        if not doc_id in self.relevance['relevance'].relevance[query]:
            self.relevance['relevance'].relevance[query].append(doc_id)

    def unset_relevant(self, query, doc_id):
        if doc_id in self.relevance['relevance'].relevance[query]:
            self.relevance['relevance'].relevance[query].remove(doc_id)


def default_index_value():
    return []
