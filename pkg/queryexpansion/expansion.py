# Final Module 3
# Global Query Expansion with WordNet

# Input: WordNet + word typed by user

# Output: Expanded Query

# Expansion required explicit confirmation by user.
# 1. When to apply this expansion? May not be appropriate when a term has many definitions. Implement chosen strategy.
# 2. Do we include only synonyms, or also hypernyms?
# 3. If the user query contains more than one word, how is the expansion performed? 
# --> I think this is implying; like in Boolean we need to go from "dog AND cat" to "(dog OR hound OR mutt) AND (cat OR feline)"; then in VSM we give them a lower weight.

from ..wordmodifiers import context
import nltk 
from nltk.corpus import wordnet 

# WordNet code adapted from these examples:
# https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
class Expansion:
	def __init__(self, ctx):
		self.ctx = ctx
		# remove stopwords (and normalization?) if thats a thing; but not stemming
		# for preprocess query, ie. stopwords, stemming, etc.
		self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
		self.filter_funcs = context.filter_funcs_for_context(ctx)

	def expand(self, query):
		expansions = {}

		query_terms = self.__clean_query(query)

		for term in query_terms:
			exp = self.__get_expansions(term)
			if exp != []:
				expansions[term] = exp

		return expansions

	# performs preprocessing on query
	def __clean_query(self, query):
		# erase brackets and split on space
		query_terms = query.replace("(", "").replace(")", "").split()

		# remove boolean keywords
		for keyword in ["AND", "OR", "AND_NOT"]:
			if keyword in query_terms:
				query_terms.remove(keyword)

		# remove regex terms (with asterisks)
		query_terms = list(filter(lambda x: not "*" in x, query_terms))

		return query_terms

	def __get_expansions(self, term):
		expansions = []
		syns = wordnet.synsets(term)

		if len(syns) > 10: # don't bother, since word has too many possible definitions	
			return []
		else:
			try:
				syn = syns[0]
				# add hypernym:
				expansions.append(syn.hypernyms()[0].lemma_names()[0].replace("_", " "))
				
				# add synonyms
				lemmas = syn.lemma_names()
				if term in lemmas: # sometimes the word shows up in its own synonyms
					lemmas.remove(term) 
				expansions.append(lemmas[0].replace("_", " "))		
			except IndexError:
				pass

		return expansions