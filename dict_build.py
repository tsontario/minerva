from pkg.dictbuilder import dictbuilder

corpus_handle = open("data/corpus/UofO_Courses.yaml", "r")
# corpus_handle = open("./test.yaml", "r")

dict_builder = dictbuilder.DictBuilder(corpus_handle, enable_stopwords=False, enable_stemming=False)
dict_builder.build()
