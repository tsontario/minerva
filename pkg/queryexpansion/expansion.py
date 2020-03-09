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

class Expansion:
	def __init__(self, ctx):
        self.ctx = ctx
        # remove stopwords (and normalization?) if thats a thing; but not stemming