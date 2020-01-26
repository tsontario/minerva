# preprocess_courses reads the raw document of Ottawa U course listings
# and outputs a processed corpus of documents
# Note that this script _does overwrite_ the corpus if it exists.
# Preventing overwrites will be done as part of the main component once
# this implementation has proven correct

import pkg.preprocessor.preprocessor as preprocessor
from os import path
import logging


infile_path = path.abspath(path.join("data", "raw", "UofO_Courses.html"))
outfile_path = path.abspath(path.join("data", "corpus", "UofO_Courses.json"))

preprocessor = preprocessor.ottawa_university_preprocessor(infile_path, outfile_path)

print("Before")
preprocessor.preprocess()
print("Done")
