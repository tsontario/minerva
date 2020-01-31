import yaml

# purpose: access documents from corpus
# input: set of document IDs
# output: set of corresponding documents (title, excerpt, full content)

def access(corpus_path, doc_ids):
	if not doc_ids:
		print("No document IDs given.")
		return []

	documents = []

	corpus_handle = open(corpus_path, "r")
	
	corpus_stream = yaml.load_all(corpus_handle, Loader=yaml.Loader)

	for doc in corpus_stream:
		if doc.id in doc_ids:
			documents.append(doc)

	return documents