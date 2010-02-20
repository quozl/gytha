from constants import *

def strnul(x):
    """ convert a NUL terminated string to a normal string
    """
    return x.split('\000')[0]

def team_decode(mask):
    """ convert a team mask to a list
    """
    x = []
    if mask & FED: x.append(teams[FED])
    if mask & ROM: x.append(teams[ROM])
    if mask & KLI: x.append(teams[KLI])
    if mask & ORI: x.append(teams[ORI])
    return x

def race_decode(n):
    """ convert a race number to letter
    """
    if n == 0: return 'F'
    elif n == 1: return 'R'
    elif n == 2: return 'K'
    elif n == 3: return 'O'
    return 'I'

slot = '0123456789abcdefghijklmnopqrstuvwxyz'

def slot_decode(n):
    try:
        return slot[n]
    except IndexError:
        print "slot_decode: input value from server %d out of range" % n

def slot_encode(n):
    return slot.find(n)

def team_colour(team):
    """ convert a team mask with a single bit set to a colour
    """
    if team == FED: return (128, 128, 0)
    if team == ROM: return (128, 0, 0)
    if team == KLI: return (0, 128, 0)
    if team == ORI: return (0, 128, 128)
    return (128, 128, 128)

def brighten(x):
    return (min(x[0]*2, 255), min(x[1]*2, 255), min(x[2]*2, 255))
