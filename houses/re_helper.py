import re

class ReException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

# generic patterns
PriceFinder = re.compile(r"(\d+)\s")
WeekMonthSelector = re.compile(r"(week|month)", re.I)
PostalCodeFinder = re.compile(r"(SW5)")

# agents specific patterns
FoxtonsAddressFinder = re.compile(r"([A-Z]!,*)")

def unique(pattern, string, convertToType=str):
    matches = pattern.findall(string)
    if (len(matches) == 1):
        return convertToType(matches[0])
        
    raise ReException("Expected 1 match, found {0} in {1} for {2}".format(len(matches), string, pattern))
