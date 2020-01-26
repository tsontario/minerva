import pdb
import re
import logging
from json import JSONEncoder
from os import path
import sys
import json

import bs4

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

# OttawaUniversityPreProcessor performs the end-to-end work of performing the ETL
# work of preparing the corpus of documents to be used by the search engine.
class OttawaUniversityPreProcessor:

    # Constructor takes an infile handle representing the raw, uncleaned, input
    # and an outfile handle to which the cleaned and processed corpus will be written
    def __init__(self, infile_path, outfile_path):
        self.infile_path = infile_path
        self.outfile_path = outfile_path
        self.corpus = []
        self.ignored = 0

    def preprocess(self):
        if path.exists(self.outfile_path):
            logger.info(
                f"Target corpus ({self.outfile_path}) already exists, skipping preprocssing."
            )
            return

        self._generate_corpus()
        print(
            f"Found {len(self.corpus)} entries out of a total of {len(self.corpus) + self.ignored}",
            "(either missing course description or french course)",
        )
        self.write_outfile()

    def write_outfile(self):
        json.dump(
            self.corpus,
            self._outfile(),
            default=self._encode_document,
            sort_keys=False,
            indent=4,
        )

    def _encode_document(self, doc):
        return {"id": doc.id, "course": doc.course.__dict__}

    def _generate_corpus(self):
        doc = bs4.BeautifulSoup(self._infile().read(), "html.parser")
        divs = doc.find_all("div", {"class": "courseblock"})
        for raw in divs:
            faculty, code, title = self._parse_course_code_and_title(raw)
            contents = self._parse_course_description(raw)
            course = Course(faculty, code, title, contents)
            if course.is_ignored():
                self.ignored += 1
                continue
            self.corpus.append(Document(course))

    def _parse_course_code_and_title(self, raw):
        title_blocks = raw.find_all("p", attrs={"class": "courseblocktitle"})
        if len(title_blocks) != 1:
            raise Exception(
                "Expected only a single p.courseblocktitle element per document"
            )
        match = re.search(
            r"^([A-Z]{3})\s*([0-9]{4,}\S?)\s+(.*)", title_blocks[0].string
        )
        if match is None:
            raise Exception(f"Couldn't parse course code from {title_blocks[0].string}")
        else:
            # We expect the faculty code, course code, and title, otherwise fail
            assert len(match.groups()) == 3
            return match.groups()

    def _parse_course_description(self, raw):
        descriptions = raw.find_all("p", {"class": "courseblockdesc"})
        if len(descriptions) > 1:
            raise Exception(
                f"Expected only a single courseblockdesc paragraph, but got: {descriptions}"
            )
        elif len(descriptions) == 0:
            return None
        return descriptions[0].text

    def _infile(self):
        return open(self.infile_path, "r")

    def _outfile(self):
        return open(self.outfile_path, "w")


# Document objects represent preprocessed objects, ready to be written to the corpus
class Document:
    DocID = 0

    def __init__(self, course):
        self.id = Document.next_id()
        self.course = course

    def __str__(self):
        return f"ID: {self.id}, Course: {self.course.faculty} {self.course.code} {self.course.title}"

    @staticmethod
    def next_id():
        Document.DocID += 1
        return Document.DocID


# Course is a simple wrapper around the course code of a given class
class Course:
    def __init__(self, faculty, code, title, contents):
        self.faculty = faculty
        self.code = code
        self.title = title
        self.contents = contents

    def __str__(self):
        return f"{self.faculty} {self.code}: {self.title}\n{self.contents}"

    # We ignore french courses, which are denoted by having the number 5 or 7 in the hundreds digit
    def is_ignored(self):
        return self.code[1] == "5" or self.code[1] == "7" or self.contents is None
