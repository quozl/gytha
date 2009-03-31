"""
rcd, receiver configurable distress calls,
generating and interpreting.

These are are binary messages for standardised tactical team
communication, sent within the otherwise textual communication
channels, inside SP_MESSAGE and CP_MESSAGE packets.

References:
netrek-server-vanilla, include/struct.h,
    struct distress for the binary format
    enum dist_type for the distress types (take, etc)
    enum target_type for the target types (none, planet, player)
    plus following comments

netrek-client-vanilla, struct.h,
    enum dist_type for the distress types known by client (different to above)

netrek-client-vanilla, input.c,
    default mapping from keyboard to distress types

"""

import struct
from constants import *

# The binary messages will only be delivered to us if we send a
# CP_FEATURE packet of RC_DISTRESS.  We may send binary messages
# regardless.

cp_feature = False # FIXME: disabled until rcd.msg.text() method fully written

# from enum dist_type
# /* help me do series */
dist_type_take = 1
dist_type_ogg = 2
dist_type_bomb = 3
dist_type_space_control = 4
dist_type_save_planet = 5
dist_type_base_ogg = 6
dist_type_help1 = 7
dist_type_help2 = 8

# /* doing series */
dist_type_escorting = 9
dist_type_ogging = 10
dist_type_bombing = 11
dist_type_controlling = 12
dist_type_asw = 13
dist_type_asbomb = 14
dist_type_doing1 = 15
dist_type_doing2 = 16

# /* other info series */
dist_type_free_beer = 17 # /* ie. player x is totally hosed now */
dist_type_no_gas = 18 # /* ie. player x has no gas */
dist_type_crippled = 19 # /* ie. player x is way hurt but may have gas */
dist_type_pickup = 20 # /* player x picked up armies */
dist_type_pop = 21 # /* there was a pop somewhere */
dist_type_carrying = 22 # /* I am carrying */
dist_type_other1 = 23
dist_type_other2 = 24

# /* just a generic distress call */
dist_type_generic = 25

class msg:
    def unpack(self, m_recipt, m_from, mesg):
        """ unpack a binary message into attributes """
        self.m_recipt = m_recipt
        self.m_from = m_from
        ( distypenflag, fuelp, dam, shld,
          etmp, wtmp, arms, sts,
          close_pl, close_en, tclose_pl, tclose_en,
          tclose_j, close_j, tclose_fr, close_fr ) = \
          struct.unpack('16B', mesg[10:26])
        self.dist_type = distypenflag & 0x1f
        self.target_type = (distypenflag & 0xc0) >> 5
        self.fuelp = fuelp & 0x7f
        self.dam = dam & 0x7f
        self.shld  = shld & 0x7f
        self.etmp = etmp & 0x7f
        self.wtmp = wtmp & 0x7f
        self.arms = arms & 0x7f
        self.sts  = sts & 0x7f
        self.close_pl = close_pl & 0x7f # closest planet to me
        self.close_en = close_en & 0x7f # closest enemy to me
        self.tclose_pl = tclose_pl & 0x7f # closest planet to cursor
        self.tclose_en  = tclose_en & 0x7f # closest enemy to cursor
        self.tclose_j = tclose_j & 0x7f # closest player to cursor
        self.close_j = close_j & 0x7f # closest player to me
        self.tclose_fr = tclose_fr & 0x7f # closest friend to cursor
        self.close_fr  = close_fr & 0x7f # closest friend to me

        # (and all this info is sent by the other client
        # automatically on every distress signal, like control/t,
        # it is magnificent in its borgishness -- Quozl)

    def text(self, galaxy):
        ship = galaxy.ship(self.m_from)
        orig = ship.mapchars
        targ = teams[self.m_recipt].upper()

        # FIXME: create a formatter for the netrek standard macro
        # format strings used by RCDs.  Meanwhile this code manually
        # translates the critical first few, as a demonstration of
        # capability.  Probably will not be called if rcd.cp_feature
        # is False.

        if self.dist_type == dist_type_take:
            # " %T%c->%O (%S) Carrying %a to %l%?%n>-1%{ @ %n%}\0"
            return '%s->%s (%s) Carrying %d to %s' % \
                   (orig, targ, ships[ship.shiptype].upper(), self.arms, \
                    galaxy.planet(self.tclose_pl).name[:3])

        if self.dist_type == dist_type_ogg:
            # " %T%c->%O Help Ogg %p at %l\0"
            return '%s->%s Help Ogg %s at %s' % \
                   (orig, targ, galaxy.planet(self.tclose_j).mapchars, \
                    galaxy.planet(self.tclose_pl).name[:3])

        if self.dist_type == dist_type_bomb:
            # " %T%c->%O %?%n>4%{bomb %l @ %n%!bomb%}\0"
            p = galaxy.planet(self.tclose_pl)
            if p.armies > 4:
                return '%s->%s bomb %s @ %d' % \
                   (orig, targ, p.name[:3], p.armies)
            else:
                return '%s->%s bomb %s' % \
                   (orig, targ, p.name)

        if self.dist_type == dist_type_space_control:
            # " %T%c->%O Help Control at %L\0"
            return '%s->%s Help Control at %s' % \
                   (orig, targ, galaxy.planet(self.tclose_pl).name[:3].upper())

        if self.dist_type == dist_type_save_planet:
            # " %T%c->%O Emergency at %L!!!!\0"
            return '%s->%s Emergency at %s!!!!' % \
                   (orig, targ, galaxy.planet(self.tclose_pl).name[:3].upper())

        if self.dist_type == dist_type_base_ogg:
            # " %T%c->%O Sync with --]> %g <[-- OGG ogg OGG base!!\0"
            return '%s->%s Sync with --]> %s <[-- OGG ogg OGG base!!' % \
                   (orig, targ, galaxy.ship(self.tclose_fr).mapchars[1:])

        print "RCD dist_type=", self.dist_type, \
              "target_type=", self.target_type, \
              "fuelp=", self.fuelp, \
              "dam=", self.dam, \
              "shld=", self.shld, \
              "etmp=", self.etmp, \
              "wtmp=", self.wtmp, \
              "arms=", self.arms, \
              "sts=", self.sts, \
              "close_pl=", self.close_pl, \
              "close_en=", self.close_en, \
              "tclose_pl=", self.tclose_pl, \
              "tclose_en=", self.tclose_en, \
              "tclose_j=", self.tclose_j, \
              "close_j=", self.close_j, \
              "tclose_fr=", self.tclose_fr, \
              "close_fr=", self.close_fr

        return None

def byte(value):
    return value & 0xff | 0x80

def norm(value, maximum):
    x = 100 * value / maximum
    if x > 0x7f: x = 0x7f
    return x & 0xff | 0x80

def pack(type, cursor, me, galaxy):
    """ pack current game state into a binary message """
    xy = (me.x, me.y)
    cpm = galaxy.closest_planet(xy) # closest planet to me
    csm = galaxy.closest_ship(xy)   # closest ship to me
    cem = galaxy.closest_enemy(xy)  # closest enemy to me
    cfm = galaxy.closest_friend(xy) # closest friend to me
    cpc = galaxy.closest_planet(cursor) # closest planet to cursor
    csc = galaxy.closest_ship(cursor)   # closest ship to cursor
    cec = galaxy.closest_enemy(cursor)  # closest enemy to cursor
    cfc = galaxy.closest_friend(cursor) # closest friend to cursor

    mesg = struct.pack('16B',
                       type,
                       norm(me.fuel, me.cap.s_maxfuel),
                       norm(me.damage, me.cap.s_maxdamage),
                       norm(me.shield, me.cap.s_maxshield),
                       norm(me.etemp, me.cap.s_maxegntemp),
                       norm(me.wtemp, me.cap.s_maxwpntemp),
                       byte(me.armies),
                       byte(me.flags),
                       byte(cpm.n),
                       byte(cem.n),
                       byte(cpc.n),
                       byte(cec.n),
                       byte(csc.n),
                       byte(csm.n),
                       byte(cfc.n),
                       byte(cfm.n),
                       )
    return mesg
