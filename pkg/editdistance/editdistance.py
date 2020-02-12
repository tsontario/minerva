import yaml

from pkg.dictionary import Dictionary
from pkg.wordmodifiers import context


class EditDistance:
    # each letter/number and its coordinates on a QWERTY keyboard (for substitution weight calculation)
    key_locations = {
        "1": [0, 0],
        "2": [0, 1],
        "3": [0, 2],
        "4": [0, 3],
        "5": [0, 4],
        "6": [0, 5],
        "7": [0, 6],
        "8": [0, 7],
        "9": [0, 8],
        "0": [0, 9],
        "q": [1, 0],
        "w": [1, 1],
        "e": [1, 2],
        "r": [1, 3],
        "t": [1, 4],
        "y": [1, 5],
        "u": [1, 6],
        "i": [1, 7],
        "o": [1, 8],
        "p": [1, 9],
        "a": [2, 0],
        "s": [2, 1],
        "d": [2, 2],
        "f": [2, 3],
        "g": [2, 4],
        "h": [2, 5],
        "j": [2, 6],
        "k": [2, 7],
        "l": [2, 8],
        "z": [3, 0],
        "x": [3, 1],
        "c": [3, 2],
        "v": [3, 3],
        "b": [3, 4],
        "n": [3, 5],
        "m": [3, 6],
    }

    def __init__(self, ctx):
        self.ctx = ctx
        self.dictionary = Dictionary(self.ctx).dictionary[ctx.dict_path()]

        # for preprocess query, ie. stopwords, stemming, etc.
        self.normalize_funcs = context.normalizer_funcs_for_context(ctx)
        self.filter_funcs = context.filter_funcs_for_context(ctx)

    # returns top N suggestions for each misspelled term in query
    def edit_distance(self, query):
        query_terms = self.__clean_query(query)
        print(query_terms)

        suggestions = {}
        for term in query_terms.items():
            if (
                not term[1] in self.dictionary.terms
            ):  # don't look for suggestions if word is recognized
                suggestions[term[0]] = self.__get_suggestions(term[1].lower())

        return suggestions

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

        # maintain dict with original term --> preprocessed term
        results = {}

        # apply normalizations/filters as specified in ctx
        for term in query_terms:
            original_term = term
            for normalize_func in self.normalize_funcs:
                term = normalize_func(term)
            term = set([term])
            for filter_func in self.filter_funcs:
                term = filter_func(term)
            results[original_term] = list(term)[0]

        return results

    # gets top N suggestions for one term
    def __get_suggestions(self, term):
        n = 5  # top n closest words will be returned
        suggestions = []

        for word in self.dictionary.terms:
            # heuristic choice: only look at dictionary terms starting with same letter
            if word[0] == term[0] and not any(
                char not in self.key_locations.keys() for char in word.lower()
            ):
                suggestions.append((word, self.__distance(term, word)))

        suggestions.sort(key=lambda s: s[1])
        return list(map(lambda s: s[0], suggestions[:n]))

    # edit distance algorithm adapted from:
    # https://www.python-course.eu/levenshtein_distance.php#Iterative-Computation-of-the-Levenshtein-Distance
    def __distance(self, source, target):
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
                    substitution_cost = 0  # ie. no substitution is required
                else:
                    substitution_cost = self.__substitution_cost(
                        source[row - 1], target[col - 1]
                    )

                # get min cost between deletion, insertion, substitution
                edit_distance[row][col] = min(
                    edit_distance[row - 1][col] + deletion_cost,
                    edit_distance[row][col - 1] + insertion_cost,
                    edit_distance[row - 1][col - 1] + substitution_cost,
                )

        return edit_distance[row][col]

    # euclidean distance between two characters on a qwerty keyboard (the 'weight')
    def __substitution_cost(self, key1, key2):
        if not (
            (key1 in self.key_locations.keys()) and (key2 in self.key_locations.keys())
        ):
            return 4  # default sub value for unrecognized chars, same as a deletion plus an insertion

        x1 = self.key_locations[key1][0]
        y1 = self.key_locations[key1][1]

        x2 = self.key_locations[key2][0]
        y2 = self.key_locations[key2][1]

        return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
