import yaml

from ..dictionary import Dictionary

class EditDistance:
    # each letter/number and its coordinates on a QWERTY keyboard (for substitution weight calculation)
    key_locations = {
        "1": [0,0], "2": [0,1], "3": [0,2], "4": [0,3], "5": [0,4], "6": [0,5], "7": [0,6], "8": [0,7], "9": [0,8], "0": [0,9],
        "q": [1,0], "w": [1,1], "e": [1,2], "r": [1,3], "t": [1,4], "y": [1,5], "u": [1,6], "i": [1,7], "o": [1,8], "p": [1,9],
        "a": [2,0],"s": [2,1], "d": [2,2], "f": [2,3], "g": [2,4], "h": [2,5], "j": [2,6], "k": [2,7], "l": [2,8],
        "z": [3,0], "x": [3,1], "c": [3,2], "v": [3,3], "b": [3,4], "n": [3,5], "m": [3,6]
    }

    def __init__(self, ctx):
        self.ctx = ctx
        self.dictionary = Dictionary(self.ctx.dict_path)

    # returns top N suggestions for each misspelled term in query
    def edit_distance(self, query):
        query_terms = query.split()

        # TODO: are stopwords removed? ensure query is preprocessed? eg. we don't want suggestions for words like 'the' if we're using stopword removal 
        for keyword in ['AND', 'OR', 'NOT']:
            if keyword in query_terms:
                query_terms.remove(keyword)

        suggestions = {}
        for term in query_terms:
            suggestions[term] = self.get_suggestions(term.lower())

        return suggestions
    
    def get_suggestions(self, term):
        n = 5 # top n closest words will be returned
        suggestions = []

        if term in self.dictionary.terms:
            return [] # no need to find suggestions for recognized words

        for word in self.dictionary.terms:
            # ignore words with accents (but allow numerical searches?)
            if not any(char not in "abcdefghijklmnopqrstuvwxyz1234567890" for char in word.lower()):
                suggestions.append((word, self.distance(term, word)))

        suggestions.sort(key=lambda s: s[1])
        result = map(lambda s: s[0], suggestions[:n])
        return result

    # edit distance algorithm adapted from: 
    # https://www.python-course.eu/levenshtein_distance.php#Iterative-Computation-of-the-Levenshtein-Distance
    def distance(self, source, target):
        rows = len(source) + 1
        cols = len(target) + 1

        deletion_cost = 2
        insertion_cost = 2
        substitution_cost = 0

        edit_distance = [[0 for x in range(cols)] for x in range(rows)]

        # source prefixes:
        for row in range(1, rows):
            edit_distance[row][0] = edit_distance[row - 1][0] + deletion_cost

        # target prefixes:
        for col in range(1, cols):
            edit_distance[0][col] = edit_distance[0][col - 1] + insertion_cost

        # filling the dynamic programming matrix
        for col in range(1, cols):
            for row in range(1, rows):
                if source[row - 1] == target[col - 1]:
                    substitution_cost = 0 # no substitution is required
                else:
                    substitution_cost = self.substitution_cost(source[row - 1], target[col - 1])

                # get min cost between deletion, insertion, substitution
                edit_distance[row][col] = min(
                    edit_distance[row - 1][col] + deletion_cost,
                    edit_distance[row][col - 1] + insertion_cost,
                    edit_distance[row - 1][col - 1] + substitution_cost,
                )

        return edit_distance[row][col]

    # euclidean distance between two characters on a qwerty keyboard
    def substitution_cost(self, key1, key2):
        x1 = self.key_locations[key1][0]
        y1 = self.key_locations[key1][1]

        x2 = self.key_locations[key2][0]
        y2 = self.key_locations[key2][1]

        return (((x1-x2)**2) + ((y1-y2)**2))**0.5 