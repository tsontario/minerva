class Stack:
    def __init__(self):
        self._stack = []

    def push(self, val):
        self._stack.append(val)
        return val

    def pop(self):
        if len(self._stack) == 0:
            return None
        return self._stack.pop()
