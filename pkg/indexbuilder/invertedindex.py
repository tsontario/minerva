class IndexKey:
    def __init__(self, term, frequency):
        self.term = term
        self.frequency = frequency

    def __repr__(self):
        return f"{self.term} ({self.frequency})"
