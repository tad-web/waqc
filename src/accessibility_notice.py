from enums import Flavor, Severity


class AccessibilityNotice:
    def __init__(self, tag, line_num, flavor, severity):
        self.tag = tag
        self.line_num = line_num
        self.flavor = flavor
        self.severity = severity
