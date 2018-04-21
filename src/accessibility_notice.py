from enums import Flavor, Severity


class AccessibilityNotice:
    def __init__(self, tag, flavor, severity):
        self.tag = tag
        self.flavor = flavor
        self.severity = severity
