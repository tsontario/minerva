# preprocess_courses reads the raw document of Ottawa U course listings
# and outputs a processed corpus of documents
# Note that this script _does overwrite_ the corpus if it exists.
# Preventing overwrites will be done as part of the main component once
# this implementation has proven correct

import pkg.preprocessor.preprocessor as preprocessor
import os
import logging

infile_path = os.path.join("data", "raw", "UofO_Courses.html")
outfile_path = os.path.join("data", "corpus", "UofO_Courses.json")

infile = open(infile_path, "r")
outfile = open(outfile_path, "w+")

preprocessor = preprocessor.ottawa_university_preprocessor(infile, outfile)

print(preprocessor)
preprocessor.preprocess()
