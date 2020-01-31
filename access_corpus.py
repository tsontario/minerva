from pkg.corpusaccess import corpusaccess as accessor

docs = accessor.access("data/corpus/UofO_Courses.yaml", [1, 2, 3])

for d in docs:
	print(d)
