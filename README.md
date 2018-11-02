# pyMqIO

Stdio/err Redirection Over Mqtt

This is a module for automatically sending all of a python programs output to an MqTT topic. The module asseses if the program was started with the -q flag , or 
if run interactively, as demonstrated:

Usage:

    >>> from redirect import *
    >>> ret = Redirect('whatever','q')
    >>> if ret.status():
    ...     from printwrap import print
    ...     print('Test')
    ... 
    >>> print('This data will not be printed to stdout. Rather it will be directed over MqTT')
    >>>


To see the output:

    mosquitto_sub -t /engines/whatever/io
    This data will not be printed to stdout. Rather it will be directed over MqTT
