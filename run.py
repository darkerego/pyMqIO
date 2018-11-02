#!/usr/bin/env python3.6

""" Initiate Redirect class with Engine name 'Test' in this example """
import sys
from redirect import *

try:
    quiet = sys.argv[1]
except IndexError:
    quiet = False


ret = Redirect('Test',quiet)
QUIET = ret.status()

if QUIET:
    from printwrap import print
    print('Quiet mode enabled')
else:
    print('Normal mode enabled')


print('Example data')
