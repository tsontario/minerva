from os import path

from pkg.indexbuilder import indexbuilder

corpus_handle = open("data/corpus/UofO_Courses.yaml", "r")
dictionary_handle = open("data/dictionary/UofOCourses.txt")
index_path = path.relpath("data/index/UofO_Courses.yaml")

index_builder = indexbuilder.IndexBuilder(corpus_handle, index_path, dictionary_handle)
breakpoint()