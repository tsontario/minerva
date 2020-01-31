class InvertedIndex:
    class IndexKey:
        def __init__(self, term, frequency):
            self.term = term
            self.frequency = frequency

    def __init__(self, contents={}):
        self.contents = contents

    def add(self, index_key, doc_ids):
        self.contents[index_key] = doc_ids
