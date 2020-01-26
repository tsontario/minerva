from pkg.dictbuilder import dictbuilder

corpus_handle = open("data/corpus/UofO_Courses.yaml", "r")

dict_builder = dictbuilder.DictBuilder(corpus_handle)
dict_builder.build()
