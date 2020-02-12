from nltk import WordPunctTokenizer


def default_tokenizer():
    return WordPunctTokenizer()


def default_enable_casefolds():
    return True


def default_enable_stopwords():
    return True


def default_enable_stemming():
    return False


def default_enable_normalization():
    return True


def default_remove_nonalphanumeric():
    return True
