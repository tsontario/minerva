from collections import defaultdict

from pkg.index import (
    OttawaUIndexBuilder,
    ReutersIndexBuilder,
    WeightedIndexAccessor,
    IndexAccessor,
)
from pkg.corpusaccess import CorpusAccessor
from pkg.wordmodifiers import context

# Module 8b. VSM Retrieval
class VectorSpaceModel:
    k = 15  # top k results, where k between 10 and 20

    def __init__(self, ctx):
        self.setup(ctx)

    def setup(self, ctx):
        self.ctx = ctx
        self.corpus_accessor = CorpusAccessor(ctx)
        self.weighted_index_accessor = WeightedIndexAccessor(ctx)
        self.index_accessor = IndexAccessor(ctx)
        # for preprocessing query, ie. stopwords, stemming, etc.
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    def search(self, ctx, query, topic, relevance=[]):
        # ensure accessors exist
        self.setup(ctx)

        # preprocess the query
        query_terms = self.__clean_query(query)

        # get all docs that have at least one of the query terms in them
        matched_doc_ids = set()
        for term in query_terms:
            docIDs = self.index_accessor.access(ctx, term).doc_ids
            for doc in docIDs:
                matched_doc_ids.add(doc)

        filtered_doc_ids = set()
        if ctx.corpus_type() == "reuters" and topic != "ALL TOPICS":
            for doc in self.corpus_accessor.access(ctx, matched_doc_ids):
                if topic in doc.topics:
                    filtered_doc_ids.add(doc.id)
        else:
            filtered_doc_ids = matched_doc_ids

        if len(filtered_doc_ids) == 0:
            return []

        weights = {}

        # do rocchio if relevance is present
        if len(relevance) > 0:
            relevant_doc_ids = [doc[1] for doc in relevance]
            not_relevant_doc_ids = [
                docID for docID in filtered_doc_ids if docID not in relevant_doc_ids
            ]

            raw_relevant = [
                (r, k[4].count(r)) for k in relevance for r in k[4].split(" ")
            ]

            beta_coefficient = 1.0 / (len(relevance))
            betas = defaultdict(lambda: 0)
            for raw in raw_relevant:
                betas[raw[0]] += raw[1]
            for query_term in query_terms:
                betas[query_term] += 1

            beta_result = {k: beta_coefficient * v for (k, v) in betas.items()}
            print(f"betas: {beta_result}")

            gamma_coefficient = 1.0 / (len(filtered_doc_ids) - len(relevant_doc_ids))
            docs = self.corpus_accessor.access(
                self.ctx, [doc_id for doc_id in not_relevant_doc_ids]
            )
            raw_not_relevant = [
                (r, k.read_queryable().count(r))
                for k in docs
                for r in k.read_queryable().split(" ")
            ]
            gammas = defaultdict(lambda: 0)
            for raw in raw_not_relevant:
                gammas[raw[0]] += raw[1]
            gamma_result = {k: gamma_coefficient * v for (k, v) in gammas.items()}
            print(f"gammas: {gamma_result}")

            query_vector = {k: 1 for k in query_terms}

            # We now have the original query vector, as well as the relevant and non-relevant biases
            for docID in filtered_doc_ids:
                weight = 0
                for term in query_terms:
                    term_weight = (
                        query_vector[term] + beta_result[term] - gamma_result[term]
                    )
                    weight += (
                        term_weight
                        * self.weighted_index_accessor.access(ctx, term)[docID]
                    )
                weights[docID] = weight

        else:
            # calculate similarity between query and document (dot product)
            for docID in filtered_doc_ids:
                weight = 0
                for term in query_terms:
                    weight += self.weighted_index_accessor.access(ctx, term)[docID]
                weights[docID] = weight


        sorted_weights = sorted(weights.items(), reverse=True, key=lambda kv: kv[1])
        # SOURCE: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

        if len(sorted_weights) < self.k:
            return sorted_weights
        else:
            return sorted_weights[: self.k]

    # performs preprocessing on query
    def __clean_query(self, query):
        # split query on space
        terms = query.split()

        # apply normalizations/filters as specified in ctx
        results = []
        for term in terms:
            for normalize_func in self.normalize_funcs:
                term = normalize_func(term)
            term = set([term])

            for filter_func in self.filter_funcs:
                term = filter_func(term)

            if list(term) != []:
                results.append(list(term)[0])

        return results
