class EditDistance:
    # each letter and its position on a QWERTY keyboard
    key_locations = {
            "q": [0,0],
            "w": [0,1],
            "e": [0,2],
            "r": [0,3],
            "t": [0,4],
            "y": [0,5],
            "u": [0,6],
            "i": [0,7],
            "o": [0,8],
            "p": [0,9],
            "a": [1,0],
            "s": [1,1],
            "d": [1,2],
            "f": [1,3],
            "g": [1,4],
            "h": [1,5],
            "j": [1,6],
            "k": [1,7],
            "l": [1,8],
            "z": [2,0],
            "x": [2,1],
            "c": [2,2],
            "v": [2,3],
            "b": [2,4],
            "n": [2,5],
            "m": [2,6]
    }

    # distance between two characters on a qwerty keyboard
    def substitution_cost(self, key1, key2):
        if not key1 in self.key_locations:
            print("Character error with " + key1)
            return 1
        if not key2 in self.key_locations:
            print("Character error with " + key2)
            return 1

        x1 = self.key_locations[key1][0]
        y1 = self.key_locations[key1][1]
        x2 = self.key_locations[key2][0]
        y2 = self.key_locations[key2][1]

        #return abs(x1-x2) + abs(y1-y2) # manhattan distance
        return (((x1-x2)**2) + ((y1-y2)**2))**0.5 # euclidean distance 
        

    #algorithm adapted from: https://www.python-course.eu/levenshtein_distance.php#Iterative-Computation-of-the-Levenshtein-Distance
    def distance(self, source, target):
        # query term is source, dictionary word is target
        source = source.lower()
        target = target.lower()

        rows = len(source) + 1
        cols = len(target) + 1

        deletion_cost = 2
        insertion_cost = 2
        substitution_cost = 0

        dist = [[0 for x in range(cols)] for x in range(rows)]

        # source prefixes:
        for row in range(1, rows):
            dist[row][0] = dist[row - 1][0] + deletion_cost

        # target prefixes:
        for col in range(1, cols):
            dist[0][col] = dist[0][col - 1] + insertion_cost

        # filling the dynamic programming matrix
        for col in range(1, cols):
            for row in range(1, rows):
                if source[row - 1] == target[col - 1]:
                    substitution_cost = 0 # no substitution is required
                else:
                    substitution_cost = self.substitution_cost(source[row - 1], target[col - 1])

                # get min cost between deletion, insertion, substitution
                dist[row][col] = min(
                    dist[row - 1][col] + deletion_cost,
                    dist[row][col - 1] + insertion_cost,
                    dist[row - 1][col - 1] + substitution_cost,
                )

        return dist[row][col]
