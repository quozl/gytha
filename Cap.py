from Constants import *

class Cap:
    """ ship capabilities, indexed by ship type """
    def __init__(self, n):
        self.n = n
        self.reset(n)
        self.seen = False

    def reset(self, n):
        self.s_type = n
        self.s_width = 20
        self.s_height = 20
        self.s_letter = ships[n][:1]
        self.s_name = ships_long[n]
        self.s_desig = ships[n]
        self.s_bitmap = n
        self.s_maxwpntemp = 1000
        self.s_maxegntemp = 1000
        x = [self.sc, self.dd, self.ca, self.bb, self.as, self.sb, self.ga, self.at]
        x[n]()

    def show(self):
        print "s_type = %d" % self.s_type
        print "s_torpspeed = %d" % self.s_torpspeed
        print "s_phaserrange = %d" % self.s_phaserrange
        print "s_maxspeed = %d" % self.s_maxspeed
        print "s_maxfuel = %d" % self.s_maxfuel
        print "s_maxshield = %d" % self.s_maxshield
        print "s_maxdamage = %d" % self.s_maxdamage
        print "s_maxwpntemp = %d" % self.s_maxwpntemp
        print "s_maxegntemp = %d" % self.s_maxegntemp
        print "s_width = %d" % self.s_width
        print "s_height = %d" % self.s_height
        print "s_maxarmies = %d" % self.s_maxarmies
        print "s_letter = %s" % self.s_letter
        print "s_name = %s" % self.s_name
        print "s_desig = %s" % self.s_desig
        print "s_bitmap = %d" % self.s_bitmap

    def sc(self):
        self.s_torpspeed = 16
        self.s_phaserrange = 75
        self.s_maxspeed = 12
        self.s_maxfuel = 5000
        self.s_maxshield = 75
        self.s_maxdamage = 75
        self.s_maxarmies = 2

    def dd(self):
        self.s_torpspeed = 14
        self.s_phaserrange = 85
        self.s_maxspeed = 10
        self.s_maxfuel = 7000
        self.s_maxshield = 85
        self.s_maxdamage = 85
        self.s_maxarmies = 5

    def ca(self):
        self.s_torpspeed = 12
        self.s_phaserrange = 100
        self.s_maxspeed = 9
        self.s_maxfuel = 10000
        self.s_maxshield = 100
        self.s_maxdamage = 100
        self.s_maxarmies = 10

    def bb(self):
        self.s_torpspeed = 12
        self.s_phaserrange = 105
        self.s_maxspeed = 8
        self.s_maxfuel = 14000
        self.s_maxshield = 130
        self.s_maxdamage = 130
        self.s_maxarmies = 6

    def as(self):
        self.s_torpspeed = 16
        self.s_phaserrange = 80
        self.s_maxspeed = 8
        self.s_maxfuel = 6000
        self.s_maxshield = 80
        self.s_maxdamage = 200
        self.s_maxegntemp = 1200
        self.s_maxarmies = 20

    def sb(self):
        self.s_torpspeed = 14
        self.s_phaserrange = 120
        self.s_maxspeed = 2
        self.s_maxfuel = 60000
        self.s_maxshield = 500
        self.s_maxdamage = 600
        self.s_maxwpntemp = 1300
        self.s_maxarmies = 25

    def ga(self):
        self.s_torpspeed = 30
        self.s_phaserrange = 10000
        self.s_maxspeed = 60
        self.s_maxfuel = 12000
        self.s_maxshield = 30000
        self.s_maxdamage = 30000
        self.s_maxwpntemp = 10000
        self.s_maxegntemp = 10000
        self.s_maxarmies = 1000

    def at(self):
        self.s_torpspeed = 30
        self.s_phaserrange = 10000
        self.s_maxspeed = 60
        self.s_maxfuel = 12000
        self.s_maxshield = 30000
        self.s_maxdamage = 30000
        self.s_maxwpntemp = 10000
        self.s_maxegntemp = 10000
        self.s_width = 28
        self.s_height = 28
        self.s_maxarmies = 1000
