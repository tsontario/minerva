import os
import sys
sys.path.append(os.path.dirname(__file__))
import ottawau

def ottawa_university_preprocessor(infile, outfile):
  return ottawau.OttawaUniversityPreProcessor(infile, outfile)

def reuters_preprocessor(infile, outfile):
  print("Not implemented")