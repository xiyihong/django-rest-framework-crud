import re
try:
    from html.parser import HTMLParser
except:
    from HTMLParser import HTMLParser

class XssHtml(HTMLParser):
    pass