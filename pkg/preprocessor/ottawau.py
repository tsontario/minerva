import bs4
import pdb
import re

# Course is a simple wrapper around the course code of a given class
class Course:
  def __init__(self, letters, numbers, title):
    self.letters = letters
    self.numbers = numbers
    self.title = title.strip()

  def __str__(self):
    return f"{self.letters} {self.numbers}: {self.title}"

  # We ignore french courses, which are denoted by having the number 7 in the hundreds digit
  def is_ignored(self):
    return self.numbers[1] == "7"

# OttawaUniversityPreProcessor performs the end-to-end work of performing the ETL
# work of preparing the corpus of documents to be used by the search engine.
class OttawaUniversityPreProcessor:

  # Constructor takes an infile handle representing the raw, uncleaned, input
  # and an outfile handle to which the cleaned and processed corpus will be written
  def __init__(self, infile, outfile):
    self.infile = infile
    self.outfile = outfile

  def preprocess(self):
    doc = bs4.BeautifulSoup(self.infile.read(), "html.parser")
    divs = (doc.find_all("div", { "class": "courseblock" }))

    doc_id = 1
    for raw in divs:
      course = None
      text = None

      # Get course code
      title_blocks = raw.find_all("p", attrs={"class": "courseblocktitle"})
      if len(title_blocks) != 1:
        raise Exception(f"Expected only a single p.courseblocktitle element per document (docID={doc_id})")
      match = re.search(r"^([A-Z]{3})\s*([0-9]{4,}\S?)\s+(.*)", title_blocks[0].string)
      if match is None:
        breakpoint()
        raise Exception(f"Couldn't parse course code from {title_blocks[0].string}")
      else:
        assert len(match.groups()) == 3
        course = Course(*match.groups())
        if not course.is_ignored():
          print(course)
