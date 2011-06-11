import random
from constants import *

def show(avail, prefix):
    x = ' '
    for team in avail:
        x += teams[team] + ' '
    print prefix + ' [' + x + ']'

def pick(mask, galaxy):
    debug = False
    if debug: print "mercenary mode, temporary debugging output follows"
    count = {}  # count of players by team
    large = IND # team with largest number of players
    small = IND # team with second largest number of players
    avail = []  # teams defined as available according to SP_MASK
    # build the count and avail lists
    for team in teams:
        count[team] = 0
    for team in teams_playable:
        if mask & team:
            avail.append(team)
    if debug: show(avail, 'avail')

    for team in teams_playable:
        for n, ship in galaxy.ships.iteritems():
            if ship.status == PFREE: continue
            if ship.team == team:
                count[team] += 1
                if count[team] > count[large]:
                    small = large
                    large = team
                else:
                    if count[team] > count[small] or large == small:
                        small = team
    if debug:
        for team in teams_playable:
            print "count", teams[team], count[team]
        print "small team", teams[small]
        print "large team", teams[large]
    # if all teams are empty, pick a random team
    if count[large] == 0:
        if debug: print "all teams empty, choosing a random team"
        n = random.choice(avail)
        if debug: print "chose", teams[n]
        return n
    # two teams are represented, a mercenary joins the second largest team
    if small in avail:
        if debug: print "players present, choosing second largest team"
        n = small
        if debug: print "chose", teams[n]
        return n
    # we are the second player to join, remove non-facing teams
    # from what is available, to avoid diagonal startup
    if small == IND:
        for diagonal in teams_diagonal:
            one, two = diagonal
            if large == one and two in avail:
                if debug: print "diag drop", teams[two]
                avail.remove(two)
            if large == two and one in avail:
                if debug: print "diag drop", teams[one]
                avail.remove(one)
        if debug: show(avail, 'avail')
    # drop the largest team from consideration if there are other
    # teams available to choose
    if len(avail) > 1 and large in avail:
        if debug: print "large drop", teams[large]
        avail.remove(large)
        if debug: show(avail, 'avail')
    # otherwise a random choice among the available teams
    if debug: print "choosing a random team"
    n = random.choice(avail)
    if debug: print "chose", teams[n]
    return n
