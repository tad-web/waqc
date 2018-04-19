from enum import Enum


class Severity(Enum):
    EXCELLENT = 1
    GOOD = 2
    INFO = 3
    WARNING = 4
    ERROR = 5


class Flavor(Enum):
    LINK = 1
    ALT_TEXT = 2
    COLOR_CONTRAST = 3
