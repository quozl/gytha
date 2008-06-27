from constants import *

def strnul(input):
    """ convert a NUL terminated string to a normal string
    """
    return input.split('\000')[0]

def team_decode(input):
    """ convert a team mask to a list
    """
    x = []
    if input & FED: x.append(teams[FED])
    if input & ROM: x.append(teams[ROM])
    if input & KLI: x.append(teams[KLI])
    if input & ORI: x.append(teams[ORI])
    return x

def race_decode(input):
    """ convert a race number to letter
    """
    if input == 0: return 'F'
    elif input == 1: return 'R'
    elif input == 2: return 'K'
    elif input == 3: return 'O'
    return 'I'

def slot_decode(input):
    return '0123456789abcdefghijklmnopqrstuvwxyz'[input]
