import os
import sys
sys.path.append(os.path.dirname(__file__))
import ottawau

def ottawa_university_preprocessor(infile_path, outfile_path):
  return ottawau.OttawaUniversityPreProcessor(infile_path, outfile_path)

def reuters_preprocessor(infile, outfile):
  print("Not implemented")