import os
import sys
from abc import ABC


def reuters_preprocessor(infile, outfile):
    print("Not implemented")


# All preprocessors implemented must expose a `preprocess` method
class Preprocessor(ABC):
    def preprocess(self):
        pass
