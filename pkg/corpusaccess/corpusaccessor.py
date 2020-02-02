import yaml

# TODO: deal with changing corpus, ie. from uOttawa to Reuters 
class CorpusAccessor:
	def __init__(self, ctx):
		self.ctx = ctx
		self.documents = {}

		with open(self.ctx.corpus_path, "r") as corpus_handle:
			corpus_stream = yaml.load_all(corpus_handle, Loader=yaml.Loader)
			for doc in corpus_stream:
				self.documents[doc.id] = doc

	def access(self, doc_ids):
		if not doc_ids:
			print("No document IDs given.")
			return []

		results = []

		for i in doc_ids:
			if i in self.documents:
				results.append(self.documents[i])
			else:
				print("Invalid document id given: " + str(i))

		return results
