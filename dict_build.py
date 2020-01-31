from pkg.dictbuilder import dictbuilder

corpus_handle = open("data/corpus/UofO_Courses.yaml", "r")
# corpus_handle = open("./test.yaml", "r")

dict_builder = dictbuilder.DictBuilder(corpus_handle, enable_stopwords=True, enable_stemming=True)
dict_builder.build()
