from collections import defaultdict

class RelevanceFeedback:
    class __RelevanceFeedback:
        def __init__(self, ctx, alpha, beta, gamma):
            self.ctx = ctx
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.relevance = defaultdict(default_index_value)
    
    def __init__(self,ctx, alpha=1, beta=0.75, gamma=0.15):
        self.relevance = RelevanceFeedback.__RelevanceFeedback(ctx, alpha, beta, gamma)
    
    def access(self, query):
        return self.relevance.relevance[query]

    def set_relevant(self, query, doc_id):
        self.relevance.relevance[query].append(doc_id)

    def unset_relevant(self, query, doc_id):
        self.relevance.relevance[query].remove(doc_id)


def default_index_value():
    return []
