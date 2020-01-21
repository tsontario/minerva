import bs4
import pdb

class OttawaUniversityPreProcessor:

  # Constructor takes an infile handle representing the raw, uncleaned, input
  # and an outfile handle to which the cleaned and processed corpus will be written
  def __init__(self, infile, outfile):
    self.infile = infile
    self.outfile = outfile

  def preprocess(self):
    doc = bs4.BeautifulSoup(self.infile.read(), "html.parser")
    divs = (doc.find_all("div", { "class": "courseblock" }))
    # TODO Parse out everything properly
    print(divs[0])
  