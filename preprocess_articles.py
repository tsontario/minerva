# preprocess_courses reads the raw document of Ottawa U course listings
# and outputs a processed corpus of documents
# Note that this script _does overwrite_ the corpus if it exists.
# Preventing overwrites will be done as part of the main component once
# this implementation has proven correct

from pkg.preprocessor import ReutersPreProcessor
from os import path
import logging


infile_path = path.abspath(path.join("data", "raw", "reuters", "*.sgm"))
outfile_path = path.abspath(path.join("data", "corpus", "reuters.yaml"))
runner = ReutersPreProcessor(infile_path, outfile_path)

print("Before")
runner.preprocess()
print("Done")
