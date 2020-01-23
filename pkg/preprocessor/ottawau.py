import pdb
import re
import logging

import bs4

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

# OttawaUniversityPreProcessor performs the end-to-end work of performing the ETL
# work of preparing the corpus of documents to be used by the search engine.
class OttawaUniversityPreProcessor:

  # Constructor takes an infile handle representing the raw, uncleaned, input
  # and an outfile handle to which the cleaned and processed corpus will be written
  def __init__(self, infile, outfile):
    self.infile = infile
    self.outfile = outfile
    self.corpus = []
    self.ignored = 0

  def preprocess(self):
    doc = bs4.BeautifulSoup(self.infile.read(), "html.parser")
    divs = (doc.find_all("div", {"class": "courseblock"}))

    for raw in divs:
      faculty, code, title = self._parse_course_code_and_title(raw)
      contents = self._parse_course_description(raw)
      course = Course(faculty, code, title, contents)
      if course.is_ignored():
        self.ignored += 1
        continue
      self.corpus.append(Document(course))
    print(f"Found {len(self.corpus)} entries out of a total of {len(self.corpus) + self.ignored}",
      "(either missing course description or french course)")

  def _parse_course_code_and_title(self, raw):
      # Get course code
      title_blocks = raw.find_all("p", attrs={"class": "courseblocktitle"})
      if len(title_blocks) != 1:
        raise Exception("Expected only a single p.courseblocktitle element per document")
      match = re.search(r"^([A-Z]{3})\s*([0-9]{4,}\S?)\s+(.*)", title_blocks[0].string)
      if match is None:
        raise Exception(f"Couldn't parse course code from {title_blocks[0].string}")
      else:
        assert len(match.groups()) == 3
        return match.groups()

  def _parse_course_description(self, raw):
    descriptions = raw.find_all("p", {"class": "courseblockdesc"})
    if len(descriptions) > 1:
      raise Exception(F"Expected only a single courseblockdesc paragraph, but got: {descriptions}")
    elif len(descriptions) == 0:
      return None
    return descriptions[0].text
