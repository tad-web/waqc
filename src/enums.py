from enum import Enum


class Severity(Enum):
  EXCELLENT = 1
  GOOD = 2
  INFO = 3
  WARNING = 4
  ERROR = 5


class Flavor(Enum):
  LINK_LABEL = 1
  ALT_TEXT = 2
  COLOR_CONTRAST = 3
  HEADER = 4
  FORM_LABEL = 5

  def __str__(self):
    return ' '.join([word.title() for word in self.name.split('_')])
