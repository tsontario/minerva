from yaml import dump_all

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

import bs4

import logging
from os import path
import sys
import glob

from .corpus import Queryable

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def reuters_preprocessor(infile_path, outfile_path):
    return ReutersPreProcessor(infile_path, outfile_path)


class ReutersPreProcessor:
    def __init__(self, infile_path, outfile_path):
        self.infile_path = infile_path
        self.outfile_path = outfile_path
        self.corpus = []
        self.ignored = 0  # Might not need this

    def preprocess(self):
        # if path.exists(self.outfile_path):
        #     logger.info(
        #         f"Target corpus ({self.outfile_path}) already exists, skipping preprocessing."
        #     )
        #     return

        self._generate_corpus()
        print(
            f"Found {len(self.corpus)} entries out of a total of {len(self.corpus) + self.ignored}"
        )
        self.write_outfile()

    def _generate_corpus(self):
        for infile in self._infiles():
            print(f"{infile}")
            with open(infile) as file:
                doc = bs4.BeautifulSoup(file)
                articles = doc.find_all("reuters")
                for article in articles:
                    topics = []
                    for tagged_topic in article.topics.find_all("d"):
                        topics.append(str(tagged_topic.string))
                    title = self._parse_attribute(article, "title")
                    print(f"{infile}: {title}")
                    body = self._parse_attribute(article, "body")
                    if body is None or title is None:
                        continue
                    self.corpus.append(
                        Article(topics, str(title.string), str(body.string))
                    )

    def write_outfile(self):
        outfile = self._outfile()
        dump_all(
            self.corpus,
            outfile,
            explicit_start=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            Dumper=Dumper,
        )

    # Unlike the Ottawa U collection, this collection is spread over multiple files,
    # hence _infile_path is the base directory, not an actual file.
    # _infiles returns a list of all files to be processed based on the provided _infile_path
    def _infiles(self):
        return glob.glob(self.infile_path)

    def _outfile(self):
        return open(self.outfile_path, "w")

    def _parse_attribute(self, article, attribute):
        raw = article.find(attribute)
        if raw is None:
            return None
        return raw.string


class Article(Queryable):
    ArticleID = 0

    def __init__(self, topics, title, body):
        self.id = Article.next_id()
        self.topics = topics
        self.title = title
        self.body = body

    def __str__(self):
        return f"ID: {self.id}, Topics: {self.topics}, Title: {self.title}, Body: {self.body}"

    def read_queryable(self):
        return f"{self.topics} {self.title} {self.body}"

    @staticmethod
    def next_id():
        Article.ArticleID += 1
        return Article.ArticleID
