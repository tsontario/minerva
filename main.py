# Throwaway script for testing preprocess package
import pkg.preprocessor.preprocessor as preprocessor
infile = open("data/raw/UofO_Courses.html", "r")
outfile = open("data/corpus/UofO_Courses.json", "w+")

preprocessor = preprocessor.ottawa_university_preprocessor(infile, outfile)

print(preprocessor)
preprocessor.preprocess()
