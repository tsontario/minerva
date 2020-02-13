from pkg.index import OttawaUIndexBuilder, WeightedIndexAccessor, IndexAccessor
from pkg.corpusaccess import CorpusAccessor
from pkg.wordmodifiers import context

# Module 8b. VSM Retrieval
class VectorSpaceModel:
	k = 15 # top k results, where k between 10 and 20
	
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
		
	def search(self, ctx, query):
		# ensure accessors exist
		self.setup(ctx)

		# preprocess the query 
		query_terms = self.__clean_query(query)

		# get all docs that have at least one of the query terms in them
		relevant_docIDs = set()
		for term in query_terms:
			docIDs = self.index_accessor.access(ctx, term).doc_ids
			for doc in docIDs:
				relevant_docIDs.add(doc)

		weights = {}
		
		# calculate similarity between query and document (dot product) 
		for docID in relevant_docIDs:
			weight = 0
			for term in query_terms:
				weight += self.weighted_index_accessor.access(ctx, term)[docID]
			weights[docID] = weight

		sorted_weights = sorted(weights.items(), reverse=True, key=lambda kv: kv[1])
		# SOURCE: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

		if len(sorted_weights) < self.k:
			return sorted_weights
		else:
			return sorted_weights[:self.k]

	# performs preprocessing on query
	def __clean_query(self, query):
		# split query on space
		query_terms = query.split()

		# apply normalizations/filters as specified in ctx
		results = []
		for term in query_terms:
			for normalize_func in self.normalize_funcs:
				term = normalize_func(term)
			term = set([term])
			
			for filter_func in self.filter_funcs:
				term = filter_func(term)

			if list(term) != []:
				results.append(list(term)[0])

		return results