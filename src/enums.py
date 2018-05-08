from enum import Enum


class Severity(Enum):
  EXCELLENT = 1
  GOOD = 2
  INFO = 3
  WARNING = 4
  ERROR = 5


class Flavor(Enum):
  SKIP_LINK = 1
  LINK_LABEL = 2
  ALT_TEXT = 3
  COLOR_CONTRAST = 4
  HEADER = 5
  FORM_LABEL = 6


  def __str__(self):
    return ' '.join([word.title() for word in self.name.split('_')])
