# tools.py

from datetime import datetime


def getTime():
    return datetime.now()


def boolean_flip(state):
    if state == False:
        return True
    else:
        return False