# Index Builder package

the `indexbuilder` package is designed to take as input a corpus of documents and a dictionary representing the cleaned (e.g. normalized, etc.) terms of the corpus. Using these inputs, an inverted index is constructed and written to file to be used for resolving search queries by other engine components. 

## Index structure

Since the index will be used both in-memory and also written to disk (to avoid needlessly recreating it on every query), we must define its representation in both media.

### In-memory structure

The `InvertedIndex` class represents a collection of `{TERM, DOCUMENT_FREQUENCY} -> [DOCUMENT_IDs...]`. Internally, `InvertedIndex` uses a dictionary to organize the key-value mappings. While this involves a bit of extra up-front work, it pays off on every query since access to a given term is done in constant time. Over the course of many queries, we end up amortizing (and then some!) the additional complexity of the upfront work.

### On-disk structure

When writing the index out to disk, the `InvertedIndex` is converted to YAML and simply written to file. Since our keys are unordered (because we use a hash table), there is no need to do any further bookkeeping.
