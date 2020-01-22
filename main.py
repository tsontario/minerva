# Throwaway script for testing preprocess package

import pkg.preprocessor.preprocessor as preprocessor
import os
infile = open(os.path.join("data", "raw", "UofO_Courses.html"), "r")
outfile = open(os.path.join("data", "corpus", "UofO_Courses.json"), "w+")

preprocessor = preprocessor.ottawa_university_preprocessor(infile, outfile)

print(preprocessor)
preprocessor.preprocess()
