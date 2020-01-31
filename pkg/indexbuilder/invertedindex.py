# Proto indices only contain TERM -> DOC_IDs mappings, and don't include the frequency count
class InvertedIndexSimple:
    class ProtoIndexKey:
        def __init__(self, term, doc_ids=[]):
            self.term = term
            self.doc_ids = doc_ids

    def __init__(self, contents={}):
        self.contents = contents

    def add(self, term, doc_id):
        self.contents[term] = doc_id


class InvertedIndexWeighted:
    class IndexKey:
        def __init__(self, term, frequency):
            self.term = term
            self.frequency = frequency

    def __init__(self, contents={}):
        self.contents = contents

    def add(self, index_key, doc_ids):
        self.contents[index_key] = doc_ids
