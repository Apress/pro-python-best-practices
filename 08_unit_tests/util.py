
from pprint import pprint
import sys

DEBUG = '-d' in sys.argv

def debug_print(*args, **kwargs):
    condition = kwargs.get('condition', True)
    if DEBUG and condition:
        for a in args:
            pprint(a)
