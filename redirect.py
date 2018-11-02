#!/usr/bin/env python3.6

"""
Standard Output and Standard Error redirection via MqTT - Skeleton
"""

import sys
import random
import paho.mqtt.client as mqtt

try:
    from config import *
except ImportError:
    mq_host='localhost';mq_port=1883;mq_user='null';mq_pass='null'

MODE = False
DEBUG = False
global QUIET
global ENGINE
global PUBTOP
engine='test'

""" Error print function - print to stderr (i.e. 2>/dev/pty) """

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

""" Substitute print function - if quiet mode, send stdout to mqtt stream, 
stderr to error log file, if not quiet mode just print data to screen """

def ioPrint(data, topic=None):
    global PUBTOP
    global QUIET
    global ENGINE
    PUBTOP="/engines/"+str(ENGINE)+"/io"
    if PUBTOP and not topic:
        topic=PUBTOP
    if QUIET:
        try:
            mqpub(data, topic=topic)
        except Exception as err:
            if DEBUG: eprint(str(err))
    else:
        print(data)

""" MqTT Publisher """

def mqpub(msg,topic='messages'):
    # Generate a random client id
    mqId="vibot-"
    letters = random.sample("abcdefghijklmnopqrstuvwxyz0123456789",6)
    for l in letters:
        mqId = mqId+l

    client = mqtt.Client(client_id=mqId, clean_session=False)
    client.username_pw_set(username=mq_user, password=mq_pass)
    client.connect(mq_host,mq_port,60)
    client.publish(topic, msg);
    client.disconnect();

""" Redirect class """

class Redirect:
    def __init__(self,engine,quiet=None):
    
        global QUIET
        global ENGINE
        global PUBTOP
        self.engine = engine
        self.quiet = quiet
        ENGINE = engine
        QUIET = quiet
        PUBTOP="/engines/"+str(ENGINE)+"/io"

    def status(self,engine=engine):
        global ENGINE
        global QUIET
        global PUBTOP

        try:
            MODE = QUIET
        except Exception as err:
           MODE = False
        else:
           if DEBUG: print('Debug: mode '+str(MODE))

        if not MODE:
            QUIET = False
        else:
            if MODE == '-q' or MODE == '--quiet' or MODE == 'quiet' or MODE == 'q':
                QUIET = True
                sys.stderr = open(ENGINE+".error.log", "a")
                eprint("Quiet mode enabled, sending output to stream to %s " % PUBTOP)

            else:
                QUIET = False
                eprint('Normal mode enabled, sending output to stdio')
                #return
            return QUIET 
