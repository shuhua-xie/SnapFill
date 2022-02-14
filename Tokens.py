import re

# Allowable tokens in the SnapFill implementation
# For now, limited to (single occurrences of):
#   tokenName               regex                               abbreviation    index num
#   startToken              '^'                                 ^               -2
#   endToken                '$'                                 $               -1
#   digits                  '\d+'                               d                0
#   alphabets               '[a-zA-Z]+'                         a                1
#   whitespace              '\s+'                               ws               2
#   Proper Case             '[A-Z][a-z]+'                       pc               3
#   CAPS                    '[A-Z]+'                            C                4
#   lowercase               '[a-z]+'                            l                5
#   Alphanumeric            '[a-zA-Z0-9]+'                      an               6
#   Proper Case w/ spaces   '[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'    pcs              7
#   CAPS w/ spaces          '[A-Z]+(?:\s+[A-Z]+)*'              Cs               8
#   lowercase w/ spaces     '[a-z]+(?:\s+[a-z]+)*'              ls               9
#   alphabets w/ spaces     '[a-zA-Z]+(?:\s+[a-zA-Z]+)*'        as              10
#   constant tokens         

# ^ and $ skipped in below lists because they are added manually
# the tokens as strings for easy equality checks
TOKENS = ["d", "a", "ws", "pc", "C", "l", "an", 
          "pcs", "Cs", "ls", "as", "^", "$"]

# compiled regex for each token
MATCHERS = [re.compile("\d+"),
            re.compile("[a-zA-Z]+"),
            re.compile("\s+"),
            re.compile("[A-Z][a-z]+"),
            re.compile("[A-Z]+"),
            re.compile("[a-z]+"),
            re.compile("[a-zA-Z0-9]+"),
            re.compile("[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*"),
            re.compile("[A-Z]+(?:\s+[A-Z]+)*"),
            re.compile("[a-z]+(?:\s+[a-z]+)*"),
            re.compile("[a-zA-Z]+(?:\s+[a-zA-Z]+)*")]
