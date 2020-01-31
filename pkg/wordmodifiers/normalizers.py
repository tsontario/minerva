import re


class Normalizer:
    @staticmethod
    def normalize_periods(text):
        # SOURCE: https://stackoverflow.com/questions/53149396/regex-to-extract-acronyms
        pattern = r"\b[A-Z](?:[\.&]?[A-Z]){1,7}\b"
        normalized_text = re.sub(pattern, lambda x: re.sub("\.", "", x.group()), text)
        return normalized_text

    @staticmethod
    def normalize_hyphens(text):
        pattern = r"\b(\w+-)+\w+\b"
        normalized_text = re.sub(pattern, lambda x: re.sub("-", " ", x.group()), text)
        return normalized_text
