import re

# Allowable tokens in the SnapFill implementation
# For now, limited to (single occurrences of):
#   tokenName       regex       abbreviation    index num
#   startToken      '^'         ^               -2
#   endToken        '$'         $               -1
#   digits          '\d+'       d                0
#   alphabets       '[a-zA-Z]+' a                1
#   whitespace      '\s'        ws               2
#   constant tokens

# ^ and $ skipped in below lists because they are added manually
# the tokens as strings for easy equality checks
TOKENS = ["d", "a", "ws", "^", "$"]

# compiled regex for each token
MATCHERS = [re.compile("\d+"),
            re.compile("[a-zA-Z]+"),
            re.compile("\s")]
