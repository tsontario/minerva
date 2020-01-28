from pkg.dictbuilder import dictbuilder

corpus_handle = open("data/corpus/UofO_Courses.yaml", "r")

dict_builder = dictbuilder.DictBuilder(corpus_handle, enable_stopwords=True)
dict_builder.build()
