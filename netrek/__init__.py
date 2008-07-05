#!/usr/bin/python
"""
    pygame netrek
    Copyright (C) 2008  James Cameron (quozl@us.netrek.org)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

http://www.cs.cmu.edu/afs/cs.cmu.edu/user/jch/netrek/humor

From: markiel@callisto.pas.rochester.edu (Andrew Markiel)
Newsgroups: rec.games.netrek
Subject: Re: Beginer!
Date: Thu, 4 Nov 93 00:33:05 GMT

STHOMAS@utcvm.utc.edu wrote:
>      I read many of the netrek postings and it seems real intresting.  Would
> anyone be willing to post instructions on how to get onto Netrek and begin
> playinf.  Particularly comand cods to get in.

Certainly! Most of them you can fish out of the code (it's written in sea),
but I can give you some pointers.

The idea behind netrek is that your race starts with 10 oysters, which
produce pearls (certain "agricultural" oysters produce pearls much faster
and thus are very valuable). The object of the game is to capture all of
the enemy's oysters by destroying all of their pearls and capturing them
with your own pearls. Each team has 8 fish attacking and defending the
oysters.

One of the most important ideas is to destroy enemy pearls (once you
destroy all the pearls on an enemy oyster, it becomes uncontrolled and
you can capture it by delivering one of your own pearls). You do this
by perching on the oyster and hitting 'b' (for bash), which causes
you to destroy the enemy pearls there.

If the oyster has more than 4 pearls, then it will be open and you
can attack all of them; however, once the oyster has less than 5, it
will close up with the pearls inside and you can't bash them anymore
(however, if you get lucky, you can bash several pearls in one swing
and thus reduce the number of pearls to below 4 before it closes up..
lobsters are very good at this).

Once the oyster is closed up, the only way to destroy the rest of the
pearls inside is to deliver your own pearls to the oyster. When you
put one of your own pearls next to the oyster, it will open up slightly
to crush it, which allows you to grab one of the ones inside and destroy
it before it closes again. Thus, for an oyster with 4 pearls, you need
to deliver 4 of your own pearls to be able to destroy all of the ones
inside, which makes the oyster uncontrolled. Then, if you put another
one of your own pearls inside, you will capture the oyster and it will
start making pearls for you.

The tricky bit is that to carry pearls around, you have to have a net
to carry them in. You make the net out of the scales of the enemy fish
that you defeat. Defeating one enemy fish gives you enough scales to
carry 2 pearls (unless you are in a lobster, in which case you have
enough to carry three pearls). They maximum number of pearls you can
carry depends on fish type. When your fish is defeated in combat,
you lose all your scales and any pearls you are carrying, and get sent
back to your spawning grounds to get a new fish. 

You fight either by tossing pebbles at the enemy fish, or by using
your scraper to scrape the scales off of them; note that after a
lot of fighting you get tired, and can't attack until you get more food
(indicated by your food stat, note that many other things, including
movement, consume food). You can get a little food anywhere, but certain
oysters provide food, which means that if you perch on a freindly food
oyster you will replace your food reserves much faster.

There are six types of fish you can control: salmon, dogfish, crabs,
bluefin, lobsters, and the mighty bass. You can always switch to
another fish by going back to your spawning ground and requesting
a new fish (and you keep whatever scales you had).

Salmon are small and fast. The have fast pebbles but very weak
scrapers, and they are too weak for most combat. They are best used
either for carrying pearls, or for bashing enemy pearls in their
backfield (every good team needs a salmon basher).

Dogfish are a little tougher than salmon, and also conserve food well.
However, they also have weak scrapers and thus aren't so useful in combat.
In fact, these fish tend to be seldom seen anymore.

Crabs are the workfish. They have lots of food and really good
scrapers, which makes them good for fighting enemy fish. Nowadays
these fish are used more than any other.

Bluefin are very big fish, but are slow and don't use food effectively,
so they tend to be useful only in close range fights near a food oyster.

Lobsters are an intersting sort of fish. They are very slow, but are
very good at bashing enemy pearls (if they get lucky, they can bash
4 pearls in one swing). They also can carry three pearls for each
enemy fish destroyed, which can be quite useful.

The bass is a very special fish. You side only can have one at a time,
and if it gets defeated it takes 30 minutes to put it back together
again. You also have a certain rank to take one. However, they are
very big and tough, and serve as a repository for pearls (where they
can't be bashed).

An interesting tactic is the bass og (it's short for ogtopus). This
is where your 8 fish surround the enemy bass (like the 8 arms of an
ogtopus). Then you wade in and beat the carp out of him. You can do
it with less fish, but it's not as effective.


Hope this helps. If you have more questions, the FAQ should be posted
in a few days.

> Stephen Thomas  University of Tennesee at Chattanooga

-Grey Elf
markiel@callisto.pas.rochester.edu

"""
import sys, time, socket, errno, select, struct, pygame, math, ctypes

# a global namespace until complexity grows too far
from netrek.cache import *
from netrek.constants import *
from netrek.mis import MultipleImageSprite
from netrek.util import *
from netrek.meta import MetaClient
from netrek.client import Client, ServerDisconnectedError
from netrek.motd import MOTD
from netrek.cap import Cap
from pygame.locals import *
import netrek.opt
import netrek.rcd

WELCOME = [
"Netrek Client Pygame",
"Copyright (C) 2008 James Cameron <quozl@us.netrek.org>",
"",
"This program comes with ABSOLUTELY NO WARRANTY; for details see source.",
"This is free software, and you are welcome to redistribute it under certain",
"conditions; see source for details."
]

ic = IC()
fc = FC()

def galactic_scale(x, y):
    """ temporary coordinate scaling, galactic to screen
    """
    return (x/100, y/100)

def tactical_scale(x, y):
    """ temporary coordinate scaling, tactical to screen, ship relative
    """
    return ((x - me.x) / 20 + 500, (y - me.y) / 20 + 500) # forward reference (me)

def galactic_descale(x, y):
    """ temporary coordinate scaling, screen to galactic
    """
    return (x*100, y*100)

def tactical_descale(x, y):
    """ temporary coordinate scaling, screen to tactical, ship relative
    """
    return ((x - 500) * 20 + me.x, (y - 500) * 20 + me.y) # forward reference (me)

def descale(x, y):
    if ph_flight == ph_galactic: # forward reference (ph_*)
        return galactic_descale(x, y)
    else:
        return tactical_descale(x, y)

def cursor():
    """ return the galactic coordinates of the mouse cursor """
    x, y = pygame.mouse.get_pos()
    return descale(x, y)

def dir_to_angle(dir):
    """ convert netrek direction to angle, approximate
    (determines how many different ship rotation images are held)
    """
    return dir * 360 / 256 / 5 * 5

def xy_to_dir(x, y):
    global me
    if ph_flight == ph_galactic: # forward reference (ph_*)
        (mx, my) = galactic_scale(me.x, me.y) # forward reference (me)
        return int((math.atan2(x - mx, my - y) / math.pi * 128.0 + 0.5))
    else:
        return int((math.atan2(x - 500, 500 - y) / math.pi * 128.0 + 0.5))

class Local:
    """ netrek game objects, corresponding to objects in the game """
    def __init__(self, n):
        self.n = n
        self.tactical = None # pygame sprite on tactical
        self.galactic = None # pygame sprite on galactic

class Planet(Local):
    """ netrek planets
        each server has a number of planets
        instances created as packets about the planets are received
        instances are listed in a dictionary of planets in the galaxy instance
    """
    def __init__(self, n):
        Local.__init__(self, n)
        self.x = -10001
        self.y = -10001
        self.name = ''
        self.sp_planet(0, 0, 0, 0)
        self.tactical = PlanetTacticalSprite(self) # forward reference
        self.galactic = PlanetGalacticSprite(self) # forward reference
        self.nearby = False

    def sp_planet_loc(self, x, y, name):
        if self.x != x or self.y != y:
            self.x = x
            self.y = y
            self.set_box(x, y)
        self.name = name

    def sp_planet(self, owner, info, flags, armies):
        self.owner = owner
        self.info = info
        self.flags = flags
        self.armies = armies

    def set_box(self, x, y):
        """ create a proximity bounding box around the planet """
        t = 13000
        wx = t * 2
        wy = t * 2
        sx = self.x - t
        sy = self.y - t
        if sx < 0:
            wx += sx
            sx = 0
        if sy < 0:
            wy += sy
            sy = 0
        self.box = pygame.Rect(sx, sy, wx, wy)

    def proximity(self, x, y):
        """ set planet visibility on tactical if we are within range """
        if self.box.collidepoint(x, y):
            if not self.nearby:
                self.nearby = True
                self.tactical.show()
        else:
            if self.nearby:
                self.nearby = False
                self.tactical.hide()

class Ship(Local):
    """ netrek ships
        each server has a number of netrek ships, normally 32 (MAXPLAYER)
        instances created as packets about the ships are received
        instances are listed in a dictionary of ships in the galaxy instance
    """
    def __init__(self, n):
        Local.__init__(self, n)
        # sp_pl_login
        self.rank = 0
        self.name = ''
        self.monitor = ''
        self.login = ''
        # sp_hostile
        self.war = 0
        self.hostile = 0
        # sp_player_info
        self.shiptype = CRUISER
        self.cap = galaxy.caps[CRUISER]
        self.team = 0
        self.mapchars = ''
        # sp_kills
        self.kills = 0
        self.sp_kills_me_shown = False
        # sp_player
        self.dir = 0
        self.speed = 0
        self.sp_player_me_speed_shown = False
        self.x = self.px = -10000
        self.y = self.py = -10000
        # sp_flags
        self.tractor = 0
        self.flags = 0
        # sp_pstatus
        self.status = PFREE
        self.tactical = ShipTacticalSprite(self) # forward reference
        self.galactic = ShipGalacticSprite(self) # forward reference
        self.ppcf = 1

    def sp_you(self, hostile, swar, armies, tractor, flags, damage, shield,
               fuel, etemp, wtemp, whydead, whodead):
        self.hostile = hostile
        self.swar = swar
        self.armies = armies
        self.tractor = tractor # FIXME: add visible tractor beams
        self.flags = flags
        self.damage = damage
        self.shield = shield
        self.fuel = fuel
        self.etemp = etemp
        self.wtemp = wtemp
        self.whydead = whydead # FIXME: display this data, on death
        self.whodead = whodead # FIXME: display this data, on death
        self.sp_you_shown = False
        global me
        if not me:
            me = self
        else:
            if me != self:
                me = self

    def sp_pl_login(self, rank, name, monitor, login):
        self.rank = rank
        self.name = name
        self.monitor = monitor
        self.login = login
        # FIXME: display this data, on player list

    def sp_hostile(self, war, hostile):
        self.war = war
        self.hostile = hostile
        # FIXME: display this data, on player list
    
    def sp_player_info(self, shiptype, team):
        self.shiptype = shiptype
        self.cap = galaxy.caps[shiptype]
        self.team = team
        self.mapchars = '%s%s' % (teams[team][:1].upper(), slot_decode(self.n))
        # FIXME: display this data, on player list

    def sp_kills(self, kills):
        global me
        if me == self:
            if self.kills != kills:
                self.sp_kills_me_shown = False
        self.kills = kills
        # FIXME: display this data, on player list
        # FIXME: show kills on tactical sprite for ship

    def sp_player(self, dir, speed, x, y):
        global me
        if me == self:
            if self.x < 0 and x > 0:
                self.px = self.x = x
                self.py = self.y = y
                galaxy.planets_proximity_check() # forward reference to enclosing class
            if self.speed != speed:
                self.sp_player_me_speed_shown = False
        self.dir = dir_to_angle(dir)
        self.speed = speed
        self.x = x
        self.y = y
        # FIXME: display speed on tactical
        
        # FIXME: potential optimisation, set a bounding box of no
        # further check required, by taking the minima and maxima of
        # the planet zones of unseen planets.
        if me == self:
            self.ppcf -= 1
            if self.ppcf < 0:
                if abs(self.x - self.px) > 1000 or abs(self.y - self.py) > 1000:
                    self.px = self.x
                    self.py = self.y
                    galaxy.planets_proximity_check() # forward reference to enclosing class
                self.ppcf = 20

    def sp_flags(self, tractor, flags):
        self.tractor = tractor
        self.flags = flags
        # FIXME: display this data, visible tractors on tactical

    def sp_pstatus(self, status):
        # store the status
        self.status = status
        # ship sprite visibility is brutally controlled by status
        # FIXME: do not show cloaked ships
        # FIXME: move visibility check to sprite class
        # FIXME: only show ships on tactical if within range of them
        # (currently we draw every ship on the tactical regardless of
        # whether the coordinates are visible)
        try:
            if status == PALIVE or status == PEXPLODE:
                self.galactic.show()
                self.tactical.show()
            else:
                self.galactic.hide()
                self.tactical.hide()
        except:
            # sprites do not exist on first call from own __init__
            # FIXME: check for attribute existence rather that use
            # brute force of exception handling
            pass

    def debug_draw(self):
        fx = 900
        fy = self.n * 30
        tx = 900 - (self.status * 10)
        ty = fy
        p = pygame.draw.line(screen, (255, 255, 255), (fx, fy), (tx, ty))
        q = pygame.draw.line(screen, (0, 0, 0), (tx, ty), (tx - 200, ty))
        return pygame.Rect.union(p, q)

    def __repr__(self):
        return 'Ship(x=%r, y=%r, team=%r)' % (self.x, self.y, self.team)
        

class Torp(Local):
    """ netrek torps
        each netrek ship has eight netrek torps
        instances created as packets about the torps are received
        instances are listed in a dictionary of torps in the galaxy instance
    """
    def __init__(self, n):
        Local.__init__(self, n)
        self.ship = galaxy.ship(n / MAXTORP) # forward reference to enclosing class
        self.fuse = 0
        self.status = TFREE
        self.sp_torp_info(0, self.status)
        self.sp_torp(0, 0, 0)
        self.tactical = TorpTacticalSprite(self) # forward reference

    def sp_torp_info(self, war, status):
        was = self.status
        self.war = war
        self.status = status
        if was == TFREE:
            if status != TFREE:
                try: self.tactical.show()
                except: pass
        else:
            if status == TFREE:
                try: self.tactical.hide()
                except: pass
                self.x = -10000
                self.y = -10000
            elif status == TEXPLODE:
                galaxy.te.append(self) # forward reference to enclosing class
                NUMDETFRAMES = 10
                self.fuse = NUMDETFRAMES * galaxy.ups / 10;
                # FIXME: animate torp explosions over local time?
                # They vary according to update rate.

    def sp_torp(self, dir, x, y):
        self.dir = dir
        self.x = x
        self.y = y

    def aging(self):
        """ if torp is exploding, decrement the explosion sequence fuse """
        if self.status == TEXPLODE:
            self.fuse -= 1
            if self.fuse <= 0:
                galaxy.te.remove(self) # forward reference to enclosing class
                self.tactical.hide()
                self.x = -10000
                self.y = -10000
                self.status = TFREE

    def debug_draw(self):
        fx = 0
        fy = self.n * 3
        tx = self.status * 50
        ty = fy
        p = pygame.draw.line(screen, (255, 255, 255), (fx, fy), (tx, ty))
        q = pygame.draw.line(screen, (0, 0, 0), (tx, ty), (tx + 200, ty))
        return pygame.Rect.union(p, q)

class Phaser(Local):
    """ netrek phasers
        each netrek ship has one netrek phaser
        instances created as packets about the phasers are received
        instances are listed in a dictionary of phasers in the galaxy instance
    """
    def __init__(self, n):
        Local.__init__(self, n)
        self.ship = galaxy.ship(n) # forward reference to enclosing class
        self.status = PHFREE
        self.want = False
        self.have = False
        self.sp_phaser(0, 0, 0, 0, 0)

    def draw(self):
        self.have = True
        if self.status == PHMISS:
            s_phaserrange = self.ship.cap.s_phaserrange
            phasedist = 6000
            factor = phasedist * s_phaserrange / 100
            angle = ( self.dir - 64 ) / 128.0 * math.pi
            tx = int(factor * math.cos(angle))
            ty = int(factor * math.sin(angle))
            (fx, fy) = (self.ship.x, self.ship.y)
            (tx, ty) = tactical_scale(fx + tx, fy + ty)
            (fx, fy) = tactical_scale(fx, fy)
        elif self.status == PHHIT2:
            (fx, fy) = (self.ship.x, self.ship.y)
            plasma.x = 100000 # FIXME: track plasma packets
            plasma.y = 100000
            (tx, ty) = tactical_scale(plasma.x, plasma.y)
        elif self.status == PHHIT:
            target = galaxy.ship(self.target) # forward reference to enclosing class
            (tx, ty) = tactical_scale(target.x, target.y)
            (fx, fy) = tactical_scale(self.ship.x, self.ship.y)
        self.txty = (tx, ty)
        self.fxfy = (fx, fy)
        return pygame.draw.line(screen, (255, 255, 255), (fx, fy), (tx, ty))

    def undraw(self, colour):
        self.have = False
        return pygame.draw.line(screen, colour, self.fxfy, self.txty)

    def sp_phaser(self, status, dir, x, y, target):
        old = self.status

        self.status = status
        self.dir = dir
        self.x = x
        self.y = y
        self.target = target

        if old == PHFREE:
            if self.status != PHFREE: self.want = True
        else:
            if self.status == PHFREE: self.want = False

class Plasma(Local):
    """ netrek plasma torps
        each netrek ship has one netrek plasma torp
        instances created as packets about the plasma torps are received
        instances are listed in a dictionary in the galaxy instance
    """
    def __init__(self, n):
        Local.__init__(self, n)
        self.ship = galaxy.ship(n) # forward reference to enclosing class
        self.status = TFREE
        self.sp_plasma_info(0, self.status)
        self.sp_plasma(0, 0)
        # self.tactical = PlasmaTacticalSprite(self)
        # FIXME: show plasma on tactical

    def sp_plasma_info(self, war, status):
        old = self.status

        self.war = war
        self.status = status

        # FIXME: this code is the same for torps, factorise it
        try:
            if old == TFREE:
                if status != TFREE:
                    self.tactical.show()
            else:
                if status == TFREE:
                    self.tactical.hide()
                elif status == TEXPLODE:
                    pass
        except:
            pass

    def sp_plasma(self, x, y):
        self.x = x
        self.y = y

class Galaxy:
    """ structure to contain all netrek game objects """
    def __init__(self):
        self.planets = {}
        self.ships = {}
        self.torps = {}
        self.te = [] # exploding torps
        self.phasers = {}
        self.plasmas = {}
        self.caps = {}
        for n in range(NUM_TYPES):
            self.caps[n] = Cap(n)
        self.motd = MOTD()
        self.ups = 5 # default if SP_FEATURE UPS is not received

    def planet(self, n):
        if not self.planets.has_key(n):
            planet = Planet(n)
            self.planets[n] = planet
        return self.planets[n]

    def planets_proximity_check(self):
        for n, planet in self.planets.iteritems():
            planet.proximity(me.x, me.y)

    def ship(self, n):
        if not self.ships.has_key(n):
            self.ships[n] = Ship(n)
        return self.ships[n]

    def ship_debug_draw(self):
        r = []
        for n, ship in self.ships.iteritems():
            r.append(ship.debug_draw())
        return r
    
    def torp(self, n):
        if not self.torps.has_key(n):
            self.torps[n] = Torp(n)
        return self.torps[n]

    def torp_aging(self):
        for t in self.te:
            t.aging()

    def torp_debug_draw(self):
        r = []
        for n, torp in self.torps.iteritems():
            r.append(torp.debug_draw())
        return r
    
    def phaser(self, n):
        if not self.phasers.has_key(n):
            self.phasers[n] = Phaser(n)
        return self.phasers[n]

    def phasers_undraw(self, colour):
        r = []
        for n, phaser in self.phasers.iteritems():
            if phaser.have: r.append(phaser.undraw(colour))
        return r
            
    def phasers_draw(self):
        r = []
        for n, phaser in self.phasers.iteritems():
            if phaser.want: r.append(phaser.draw())
        return r

    def plasma(self, n):
        if not self.plasmas.has_key(n):
            self.plasmas[n] = Plasma(n)
        return self.plasmas[n]

    def cap(self, n):
        if not self.caps.has_key(n):
            self.caps[n] = Cap(n)
        return self.caps[n]

    def is_enemy(self, thing):
        return thing.team != me.team

    def is_friend(self, thing):
        return thing.team == me.team

    def is_alive(self, thing):
        return thing.status == PALIVE

    def closest(self, xy, things, checks):
        """ return the closest thing to galactic coordinates,
            ignoring me,
            but return me if nothing found.
        """
        x, y = xy
        closest = me
        minimum = GWIDTH**2
        for n, thing in things.iteritems():
            if thing == me: continue
            disinterest = False
            for check in checks:
                if not check(thing):
                    disinterest = True
                    break
            if disinterest: continue
            distance = (thing.x - x)**2 + (thing.y - y)**2
            if distance < minimum:
                closest = thing
                minimum = distance
        return closest

    def closest_planet(self, xy):
        """ return the closest planet to galactic coordinates """
        return self.closest(xy, self.planets, [])

    def closest_ship(self, xy):
        """ return the closest ship to galactic coordinates """
        return self.closest(xy, self.ships, [self.is_alive])

    def closest_planet(self, xy):
        """ return the closest planet to galactic coordinates """
        return self.closest(xy, self.planets, [])

    def closest_enemy(self, xy):
        """ return the closest hostile player to coordinates """
        return self.closest(xy, self.ships, [self.is_enemy, self.is_alive])

    def closest_friend(self, xy):
        """ return the closest friendly player to coordinates """
        return self.closest(xy, self.ships, [self.is_friend, self.is_alive])

    def sp_message(self, m_flags, m_recipt, m_from, mesg):
        # FIXME: this is temporary processing of distress messages,
        # depending on the type of message it should be portrayed.
        if m_flags == (MVALID | MTEAM | MDISTR):
            d = rcd.msg()
            d.unpack(m_recipt, m_from, mesg)
            print d.text(galaxy)
        else:
            print strnul(mesg)
        # FIXME: display the message

galaxy = Galaxy()
me = None

class PlanetSprite(MultipleImageSprite):
    """ netrek planet sprites
    """
    def __init__(self, planet):
        self.planet = planet
        self.old_armies = planet.armies
        self.old_name = planet.name
        self.old_flags = planet.flags
        self.old_x = planet.x
        self.old_y = planet.y
        self.old_owner = planet.owner
        MultipleImageSprite.__init__(self)

class PlanetGalacticSprite(PlanetSprite):
    """ netrek planet sprite on galactic """
    def __init__(self, planet):
        PlanetSprite.__init__(self, planet)
        self.pick()
        g_planets.add(self)

    def pick(self):
        self.mi_begin()
        # IMAGERY: planet-???-30x30.png
        image = ic.get("planet-" + teams[self.planet.owner] + "-30x30.png")
        self.mi_add_image(image)
        
        # FIXME: render planet owner, flags and armies
        
        image = pygame.Surface((120, 120), pygame.SRCALPHA, 32)
        font = fc.get('DejaVuSans.ttf', 8)
        message = "%s" % (self.planet.name)
        text = font.render(message, 1, (128, 128, 128))
        rect = text.get_rect(centerx=60, bottom=90)
        image.blit(text, rect)
        self.mi_add_image(image)
        self.mi_commit()

    def update(self):
        if self.planet.owner != self.old_owner or self.planet.name != self.old_name:
            self.pick()
            self.rect.center = galactic_scale(self.planet.x, self.planet.y)
            self.old_owner = self.planet.owner
            self.old_name = self.planet.name
        if self.planet.x != self.old_x or self.planet.y != self.old_y:
            self.rect.center = galactic_scale(self.planet.x, self.planet.y)
            self.old_x = self.planet.x
            self.old_y = self.planet.y
            
class PlanetTacticalSprite(PlanetSprite):
    """ netrek planet sprite on tactical """
    def __init__(self, planet):
        self.me_old_x = -1
        self.me_old_y = -1
        PlanetSprite.__init__(self, planet)
        self.pick()

    def show(self):
        t_planets.add(self)

    def hide(self):
        t_planets.remove(self)

    def pick(self):
        self.mi_begin()
        # IMAGERY: planet-???.png
        image = ic.get("planet-" + teams[self.planet.owner] + ".png")
        self.mi_add_image(image)

        # IMAGERY: planet-overlay-*.png
        if self.planet.armies > 4 and self.planet.owner != me.team:
            self.mi_add_image(ic.get('planet-overlay-attack.png'))
            # FIXME: show attack ring for unscanned planets as well?
        if self.planet.armies > 4:
            self.mi_add_image(ic.get('planet-overlay-army.png'))
        if self.planet.flags & PLREPAIR:
            self.mi_add_image(ic.get('planet-overlay-repair.png'))
        if self.planet.flags & PLFUEL:
            self.mi_add_image(ic.get('planet-overlay-fuel.png'))
        # FIXME: cache the static flags surfaces here, they will rarely change

        image = pygame.Surface((120, 120), pygame.SRCALPHA, 32)
        font = fc.get('DejaVuSans.ttf', 18)
        message = "%s" % (self.planet.name)
        text = font.render(message, 1, (92, 92, 92))
        rect = text.get_rect(centerx=60, bottom=120)
        # FIXME: name may not fit within surface
        # FIXME: cache this surface here, it will rarely change
        image.blit(text, rect)
        self.mi_add_image(image)
        self.mi_commit()
        
    def update(self):
        if self.planet.owner != self.old_owner or \
               self.planet.name != self.old_name or \
               self.planet.flags != self.old_flags or \
               self.planet.armies != self.old_armies:
            self.pick()
            self.old_owner = self.planet.owner
            self.old_name = self.planet.name
            self.old_flags = self.planet.flags
            self.old_armies = self.planet.armies
            self.rect.center = tactical_scale(self.planet.x, self.planet.y)
        if self.planet.x != self.old_x or \
               self.planet.y != self.old_y or \
               me.x != self.me_old_x or \
               me.y != self.me_old_y:
            self.rect.center = tactical_scale(self.planet.x, self.planet.y)
            self.old_x = self.planet.x
            self.old_y = self.planet.y
            self.me_old_x = me.x
            self.me_old_y = me.y
            
class ShipSprite(MultipleImageSprite):
    def __init__(self, ship):
        self.ship = ship
        self.old_status_tuple = None
        MultipleImageSprite.__init__(self)

class ShipGalacticSprite(ShipSprite):
    """ netrek ship sprites
    """
    # FIXME: a non-moving ship does not appear
    def __init__(self, ship):
        ShipSprite.__init__(self, ship)
        self.pick()

    def update(self):
        status_tuple = self.ship.dir, self.ship.team, self.ship.shiptype, self.ship.status, self.ship.flags
        if status_tuple != self.old_status_tuple:
            self.old_status_tuple = status_tuple
            self.pick()
        self.rect.center = galactic_scale(self.ship.x, self.ship.y)

    def pick(self):
        # FIXME: obtain imagery for galactic view
        # IMAGERY: ???-8x8.png
        self.image = ic.get_rotated(teams[self.ship.team]+"-8x8.png", self.ship.dir)
        self.rect = self.image.get_rect()
        
    def show(self):
        g_players.add(self)

    def hide(self):
        g_players.remove(self)

class ShipTacticalSprite(ShipSprite):
    """ netrek ship sprites
    """
    def __init__(self, ship):
        ShipSprite.__init__(self, ship)
        self.pick()

    def update(self):
        status_tuple = self.ship.dir, self.ship.team, self.ship.shiptype, self.ship.status, self.ship.flags
        if status_tuple != self.old_status_tuple:
            self.old_status_tuple = status_tuple
            self.pick()
        self.rect.center = tactical_scale(self.ship.x, self.ship.y)

    def pick(self):
        self.mi_begin()
        if self.ship.status == PEXPLODE:
            # FIXME: animate explosion
            # FIXME: initial frames to show explosion developing over ship
            # IMAGERY: explosion.png
            self.mi_add_image(ic.get('explosion.png'))
        else:
            # FIXME: obtain imagery for galactic view
            # IMAGERY: ???-??-40x40.png
            if self.ship.shiptype != STARBASE:
                rotation = self.ship.dir
            else:
                rotation = 0
            try:
                self.mi_add_image(ic.get_rotated(teams[self.ship.team]+'-'+ships[self.ship.shiptype]+"-40x40.png", rotation))
            except:
                self.mi_add_image(ic.get_rotated('netrek.png', rotation))

        # FIXME: filter for visibility by distance from me
        status = self.ship.status
        flags = self.ship.flags

        # ship number
        image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
        font = fc.get('DejaVuSans.ttf', 24)
        message = slot_decode(self.ship.n)
        colour = (255, 255, 255)
        if flags & PFPRACTR:
            colour = (0, 255, 0)
        elif flags & PFROBOT:
            colour = (255, 0, 0)
        elif flags & PFBPROBOT:
            colour = (0, 0, 255)
        elif flags & PFDOCKOK:
            colour = (0, 255, 255)
        text = font.render(message, 1, colour)
        rect = text.get_rect(center=(20, 20))
        # FIXME: cache this surface here, it will never change
        image.blit(text, rect)
        self.mi_add_image(image)

        if status == PALIVE:
            if flags & PFCLOAK:
                # IMAGERY: ship-cloak.png
                self.mi_add_image(ic.get('ship-cloak.png'))
            if flags & PFSHIELD and (self.ship == me or not flags & PFCLOAK):
                # IMAGERY: shield-80x80.png
                self.mi_add_image(ic.get('shield-80x80.png'))

        # FIXME: not show or show differently if PFCLOAK
        self.mi_commit()
        
    def show(self):
        t_players.add(self)

    def hide(self):
        t_players.remove(self)

class TorpSprite(pygame.sprite.Sprite):
    def __init__(self, torp):
        self.torp = torp
        self.old_status = torp.status
        pygame.sprite.Sprite.__init__(self)

class TorpTacticalSprite(TorpSprite):
    """ netrek torp sprites
    """
    def __init__(self, torp):
        TorpSprite.__init__(self, torp)
        self.teams = { IND: 'torp-ind.png', FED: 'torp-fed.png', ROM: 'torp-rom.png', KLI: 'torp-kli.png', ORI: 'torp-ori.png' }
        self.types = { TFREE: 'netrek.png',
                       TEXPLODE: 'torp-explode-200.png',
                       TDET: 'torp-det.png',
                       TOFF: 'torp-off.png',
                       TSTRAIGHT: 'torp-straight.png' }
        self.pick()

    def update(self):
        # torp image changes only while exploding or change of status
        if self.torp.status == TEXPLODE:
            self.old_status = self.torp.status
            self.pick()
        else:
            if self.torp.status != self.old_status:
                self.old_status = self.torp.status
                self.pick()
        self.rect.center = tactical_scale(self.torp.x, self.torp.y)
    
    def pick(self):
        if self.torp.status == TMOVE:
            if self.torp.ship == me:
                # IMAGERY: torp-me.png
                self.image = ic.get('torp-me.png')
            else:
                # IMAGERY: torp-???.png
                self.image = ic.get(self.teams[self.torp.ship.team])
        elif self.torp.status == TEXPLODE:
            # IMAGERY: torp-explode.png
            # IMAGERY: torp-explode-*.png
            exp = ['torp-explode-20.png', 'torp-explode-40.png', 'torp-explode-60.png', 'torp-explode-80.png', 'torp-explode-100.png', 'torp-explode-120.png', 'torp-explode-140.png', 'torp-explode-160.png', 'torp-explode-180.png', 'torp-explode-200.png']
            try:
                self.image = ic.get(exp[self.torp.fuse])
            except:
                self.image = ic.get('torp-explode.png')
        else:
            self.image = ic.get('netrek.png')
        
        self.rect = self.image.get_rect()
        
    def show(self):
        t_torps.add(self)

    def hide(self):
        t_torps.remove(self)

class Borders:
    """ netrek borders
    """
    def __init__(self):
        self.lines = []
        self.rect = []
        proximity = 0.90 # how close before wall appears
        threshold = n = int(GWIDTH / 10.0 * proximity)
        self.inner = pygame.Rect(n, n, GWIDTH-n-n, GWIDTH-n-n)
        # FIXME: proximity customisation option

    def line(self, sx, sy, ex, ey):
        self.lines.append((sx, sy, ex, ey))
        return pygame.draw.line(screen, (255, 0, 0), (sx, sy), (ex, ey))

    def limit(self, v1, v2):
        return (max(0, v1), min(999, v2))

    def draw(self):
        self.lines = []
        self.rect = []

        if self.inner.collidepoint(me.x, me.y): return self.rect
        x1, y1 = tactical_scale(0, 0)
        x2, y2 = tactical_scale(GWIDTH, GWIDTH)
        if 0 < x1 < 500: # left edge
            (sy, ey) = self.limit(y1, y2)
            self.rect.append(self.line(x1, sy, x1, ey))
        if 0 < y1 < 500: # top edge
            (sx, ex) = self.limit(x1, x2)
            self.rect.append(self.line(sx, y1, ex, y1))
        if 500 < x2 < 1000: # right edge
            (sy, ey) = self.limit(y1, y2)
            self.rect.append(self.line(x2, sy, x2, ey))
        if 500 < y2 < 1000: # bottom edge
            (sx, ex) = self.limit(x1, x2)
            self.rect.append(self.line(sx, y2, ex, y2))
        return self.rect

    def undraw(self, colour):
        for (sx, sy, ex, ey) in self.lines:
            pygame.draw.line(screen, colour, (sx, sy), (ex, ey))
        return self.rect

    def draw_debug_planet_proximity_boxes(self):
        for n, planet in galaxy.planets.iteritems():
            (x1, y1, w, h) = planet.box
            x2 = x1 + w
            y2 = y1 + h
            x1, y1 = tactical_scale(x1, y1)
            x2, y2 = tactical_scale(x2, y2)
            self.rect.append(self.line(x1, y1, x2, y2))
            self.rect.append(self.line(x1, y2, x1, y2))

class ReportSprite(pygame.sprite.Sprite):
    """ netrek reports
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = fc.get('DejaVuSansMono.ttf', 20)
        self.fuel = self.damage = self.shield = self.armies = 0
        self.image = self.font.render('--', 1, (255, 255, 255))
        self.rect = self.image.get_rect(centerx=500, bottom=999)

    def update(self):
        if me.sp_you_shown and me.sp_player_me_speed_shown and me.sp_kills_me_shown: return
        me.sp_you_shown = True
        me.sp_player_me_speed_shown = True
        me.sp_kills_me_shown = True
        self.pick()

    def flags(self):
        f = me.flags
        if f & PFPRESS: f ^= PFTRACT
        r = ''
        x = ['SHIELDS',      'REPAIRING',     'BOMBING',       'ORBITING',
             'CLOAKED',      'WEAPONS-HOT',   'ENGINES-HOT',   'ROBOT',
             'BEAM-UP',      'BEAM-DOWN',     'SELF-DESTRUCT', None,
             'YELLOW-ALERT', 'RED-ALERT',     'SHIP-LOCK',     'PLANET-LOCK',
             'COPILOT',      'DECLARING-WAR', 'PRACTICE',      'DOCKED',
             'REFIT',        'REFITTING',     'TRACTOR',       'PRESSOR',
             'DOCKING-OK',   'SEEN',          'CYBORG',        'OBSERVING',
             None,           None,            'TRANSWARP',     'BPROBOT']
        for n in range(32):
            if f & (1 << n):
                if x[n]:
                    r += x[n] + ' '
        return r

    def pick(self):
        x = ' '
        if me.armies > 0:                  x += "A %d " % me.armies
        if me.kills  > 0:                  x += "K %.2f " % (me.kills / 100.0)
        if me.shiptype != STARBASE:
            if me.speed > 0:               x += "S %d " % me.speed
        else:
            if me.speed != me.cap.s_maxspeed: x += "S %d " % me.speed
        if me.fuel   < me.cap.s_maxfuel:   x += "F %d " % me.fuel
        if me.damage > 0:                  x += "D %d " % me.damage
        if me.shield < me.cap.s_maxshield: x += "S %d " % me.shield
        if me.etemp  > 0:                  x += "E %d " % (me.etemp / 10)
        if me.wtemp  > 0:                  x += "W %d " % (me.wtemp / 10)
        x += self.flags()
        self.text = x
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect(centerx=500, bottom=999)

class WarningSprite(pygame.sprite.Sprite):
    """ netrek warnings
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = fc.get('DejaVuSans.ttf', 24)
        self.last = ''
        self.time = 0
        self.pick('')

    def update(self):
        if sp_warning.seen: return
        sp_warning.seen = True
        text = sp_warning.text
        if self.last != text:
            self.last = text
            self.pick(text)
            self.time = 1000
            length = len(text)
            if length > 32: self.time = 2500
            if length > 64: self.time = 5000
        pygame.time.set_timer(pygame.USEREVENT+2, self.time)

    def ue(self, event):
        pygame.time.set_timer(pygame.USEREVENT+2, 0)
        self.pick('')

    def pick(self, text):
        self.image = self.font.render(text, 1, (255, 0, 0))
        self.rect = self.image.get_rect(centerx=500, top=0)

""" assorted sprites
"""

class SpriteBacked(pygame.sprite.Sprite):
    """ a sprite on the existing background """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def clear(self):
        return screen.blit(self.background, self.rect)

    def suck(self):
        self.background = screen.subsurface(self.rect).copy()

    def blit(self):
        return screen.blit(self.image, self.rect)

    def draw(self):
        self.suck()
        return self.blit()

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Clickable():
    """ a clickable screen object """
    def __init__(self, clicked):
        self.clicked = clicked
        self.arm = False

    def md(self, event):
        if not self.rect.collidepoint(event.pos[0], event.pos[1]):
            self.arm = False
            return False
        if event.button != 1:
            self.arm = False
            return True
        self.arm = True
        return True

    def mu(self, event):
        if not self.rect.collidepoint(event.pos[0], event.pos[1]):
            self.arm = False
            return False
        if event.button != 1:
            self.arm = False
            return True
        if not self.arm: return True
        self.clicked(event)
        self.arm = False
        return True

class Icon(SpriteBacked):
    """ a sprite for icons, a simple image """
    def __init__(self, name, x, y):
        self.image = ic.get(name)
        self.rect = self.image.get_rect(centerx=x, centery=y)
        SpriteBacked.__init__(self)

class RotatingIcon(SpriteBacked):
    """ a sprite for rotating icons """
    def __init__(self, name, x, y, angle):
        self.name = name
        self.x = x
        self.y = y
        self.angle = angle / 5 * 5
        self.rotate(angle)
        SpriteBacked.__init__(self)

    def rotate(self, angle):
        self.angle = angle / 5 * 5
        self.image = ic.get_rotated(self.name, angle)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

class Text(SpriteBacked):
    def __init__(self, text, x, y, size=18, colour=(255, 255, 255)):
        font = fc.get('DejaVuSans.ttf', size)
        self.image = font.render(text, 1, colour)
        self.rect = self.image.get_rect(left=x, centery=y)
        SpriteBacked.__init__(self)

class TextsLine(SpriteBacked):
    def __init__(self, text, x, y, size=18):
        font = fc.get('DejaVuSansMono.ttf', size)
        self.image = font.render(text, 1, (255, 255, 255))
        self.rect = self.image.get_rect(left=x, top=y)
        SpriteBacked.__init__(self)
        
class Texts:
    def __init__(self, texts, x, y, lines=24, size=18):
        self.group = pygame.sprite.OrderedUpdates()
        self.left = x
        self.top = self.y = y
        self.lines = lines
        self.size = size
        for row in texts:
            self._new(row)
            self.lines -= 1
            if self.lines < 1: break
        self.draw()

    def _new(self, text):
        sprite = TextsLine(text, self.left, self.y, self.size)
        self.y = sprite.rect.bottom
        self.group.add(sprite)
        return sprite

    def draw(self):
        self.rects = self.group.draw(screen)

    def add(self, text):
        if self.lines < 1: return None
        sprite = self._new(text)
        sprite.draw()
        return sprite

class Field:
    def __init__(self, prompt, value, x, y):
        self.value = value
        self.fn = fn = fc.get('DejaVuSans.ttf', 36)
        self.sw = sw = screen.get_width()
        self.sh = sh = screen.get_height()
        # place prompt on screen
        self.ps = ps = fn.render(prompt, 1, (255, 255, 255))
        self.pc = pc = (x, y)
        self.pr = pr = ps.get_rect(topright=pc)
        self.pg = screen.subsurface(self.pr).copy()
        r1 = screen.blit(ps, pr)
        # highlight entry area
        self.br = pygame.Rect(pr.right, pr.top, sw - pr.right - 300, pr.height)
        self.bg = screen.subsurface(self.br).copy()
        pygame.display.update(r1)
        self.enter()
        
    def highlight(self):
        return screen.fill((0,127,0), self.br)

    def unhighlight(self):
        return screen.blit(self.bg, self.br)

    def draw(self):
        as = self.fn.render(self.value, 1, (255, 255, 255))
        ar = as.get_rect(topleft=self.pc)
        ar.left = self.pr.right
        return screen.blit(as, ar)
        
    def undraw(self):
        return screen.blit(self.pg, self.pr)

    def redraw(self):
        r1 = self.highlight()
        r2 = self.draw()
        pygame.display.update([r1, r2])

    def leave(self):
        r1 = self.unhighlight()
        r2 = self.draw()
        pygame.display.update([r1, r2])
        
    def enter(self):
        r1 = self.highlight()
        r2 = self.draw()
        pygame.display.update([r1, r2])
        
    def append(self, char):
        self.value = self.value + char
        r1 = self.draw()
        pygame.display.update(r1)
        
    def backspace(self):
        self.value = self.value[:-1]
        self.redraw()

    def delete(self):
        self.value = ""
        self.redraw()

class Button(Text, Clickable):
    def __init__(self, clicked, text, x, y, size, colour):
        self.text = text
        Text.__init__(self, text, x, y, size, colour)
        Clickable.__init__(self, clicked)

""" animations
"""

class Bouncer():
    """ two torps following an orbital ellipse around an invisible mass """
    def __init__(self, ex, ey, cx, cy, n1='torp-me.png', n2='torp-me.png'):
        self.ex = ex
        self.ey = ey
        self.cx = cx
        self.cy = cy
        self.l = Icon(n1, self.cx+50, self.cy)
        self.l.draw()
        self.r = Icon(n2, self.cx-50, self.cy)
        self.r.draw()

    def update(self, pos, max):
        r = []
        r.append(self.l.clear())
        r.append(self.r.clear())
        x = self.ex * math.sin(pos * math.pi / max)
        y = self.ey * math.cos(pos * math.pi / max)
        self.l.move(500 - x, self.cy - y)
        self.r.move(500 + x, self.cy + y)
        r.append(self.l.draw())
        r.append(self.r.draw())
        pygame.display.update(r)

""" netrek protocol documentation, from server include/packets.h

	general protocol state outline

	starting state

	CP_SOCKET
	CP_FEATURE, optional, to indicate feature packets are known
	SP_MOTD
	SP_FEATURE, only if CP_FEATURE was seen
	SP_QUEUE, optional, repeats until slot is available
	SP_YOU, indicates slot number assigned

	login state, player slot status is POUTFIT
	client shows name and password prompt and accepts input

	CP_LOGIN
	CP_FEATURE
	SP_LOGIN
	SP_YOU
	SP_PLAYER_INFO
	various other server packets

	outfit state, player slot status is POUTFIT
	client shows team selection window

	SP_MASK, sent regularly during outfit

	client accepts team selection input
	CP_OUTFIT
	SP_PICKOK, signals server acceptance of alive state

	alive state,
	server places ship in game and play begins

	SP_PSTATUS, indicates PDEAD state
	client animates explosion

	SP_PSTATUS, indicates POUTFIT state
	clients returns to team selection window

	CP_QUIT
	CP_BYE
"""

""" client originated packets
"""

cp_table = {}

class ClientPacket(type):
    def __new__(cls, name, bases, dct):
        client_packet = type.__new__(cls, name, bases, dct)

        if name.startswith('CP_'):
            cp_table[client_packet.code] = client_packet.format
            globals()[name.lower()] = client_packet()

        return client_packet

class CP:
    __metaclass__ = ClientPacket

    code = -1
    format = ''

    def data(self, *args):
        if opt.cp: print self.__class__.__name__, args
        return struct.pack(self.format, self.code, *args)

class CP_SOCKET(CP):
    code = 27
    format = '!bbbxI'

    def data(self):
        if opt.cp: print "CP_SOCKET"
        return struct.pack(self.format, self.code, 4, 10, 0)

class CP_BYE(CP):
    code = 29
    format = '!bxxx'

    def data(self):
        if opt.cp: print "CP_BYE"
        return struct.pack(self.format, self.code)

class CP_LOGIN(CP):
    code = 8
    format = '!bbxx16s16s16s' 

    def data(self, query, name, password, login):
        if opt.cp: print "CP_LOGIN query=",query,"name=",name
        return struct.pack(self.format, self.code, query, name, password, login)

class CP_OUTFIT(CP):
    code = 9
    format = '!bbbx'

    def data(self, race, ship=ASSAULT):
        if opt.cp: print "CP_OUTFIT team=",race_decode(race),"ship=",ship
        return struct.pack(self.format, self.code, race, ship)

class CP_SPEED(CP):
    code = 2
    format = '!bbxx'

    def data(self, speed):
        if opt.cp: print "CP_SPEED speed=",speed
        return struct.pack(self.format, self.code, speed)

class CP_DIRECTION(CP):
    code = 3
    format = '!bBxx'

    def data(self, direction):
        if opt.cp: print "CP_DIRECTION direction=",direction
        return struct.pack(self.format, self.code, direction & 255)

class CP_PLANLOCK(CP):
    code = 15
    format = '!bbxx'

    def data(self, pnum):
        if opt.cp: print "CP_PLANLOCK pnum=",pnum
        return struct.pack(self.format, self.code, pnum)

class CP_PLAYLOCK(CP):
    code = 16
    format = '!bbxx'

    def data(self, pnum):
        if opt.cp: print "CP_PLAYLOCK pnum=",pnum
        return struct.pack(self.format, self.code, pnum)

class CP_UPDATES(CP):
    code = 31
    format = '!bxxxI'

    def data(self, usecs):
        if opt.cp: print "CP_UPDATES usecs=",usecs
        return struct.pack(self.format, self.code, usecs)

class CP_BOMB(CP):
    code = 17
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_BOMB state=",state
        return struct.pack(self.format, self.code, state)

class CP_BEAM(CP):
    code = 18
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_BEAM state=",state
        return struct.pack(self.format, self.code, state)

class CP_CLOAK(CP):
    code = 19
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_CLOAK state=",state
        return struct.pack(self.format, self.code, state)

class CP_REPAIR(CP):
    code = 13
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_REPAIR state=",state
        return struct.pack(self.format, self.code, state)

class CP_SHIELD(CP):
    code = 12
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_SHIELD state=",state
        return struct.pack(self.format, self.code, state)

class CP_MESSAGE(CP):
    code = 1
    format = "!bBBx80s"

    def data(self, group, indiv, mesg):
        if opt.cp: print "CP_MESSAGE group=",group,"indiv=",indiv,"mesg=",mesg
        return struct.pack(self.format, self.code, group, indiv, mesg)

class CP_PHASER(CP):
    code = 4
    format = '!bBxx'

    def data(self, direction):
        if opt.cp: print "CP_PHASER direction=",direction
        return struct.pack(self.format, self.code, direction & 255)

class CP_PLASMA(CP):
    code = 5
    format = '!bBxx'

    def data(self, direction):
        if opt.cp: print "CP_PLASMA direction=",direction
        return struct.pack(self.format, self.code, direction)

class CP_TORP(CP):
    code = 6
    format = '!bBxx'

    def data(self, direction):
        if opt.cp: print "CP_TORP direction=",direction
        return struct.pack(self.format, self.code, direction & 255)

class CP_QUIT(CP):
    code = 7
    format = '!bxxx'

    def data(self):
        if opt.cp: print "CP_QUIT"
        return struct.pack(self.format, self.code)
        # FIXME: on quit, no teams available for selection, should
        # drop out rather than show outfit window.

class CP_WAR(CP):
    code = 10
    format = '!bbxx'

    def data(self, newmask):
        if opt.cp: print "CP_WAR newmask=",newmask
        return struct.pack(self.format, self.code, newmask)

class CP_PRACTR(CP):
    code = 11
    format = '!bxxx'

    def data(self):
        if opt.cp: print "CP_PRACTR"
        return struct.pack(self.format, self.code)

class CP_ORBIT(CP):
    code = 14
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_ORBIT =",state
        return struct.pack(self.format, self.code, state)

class CP_DET_TORPS(CP):
    code = 20
    format = '!bxxx'

    def data(self):
        if opt.cp: print "CP_DET_TORPS"
        return struct.pack(self.format, self.code)

class CP_DET_MYTORP(CP):
    code = 21
    format = '!bxh'

    def data(self, tnum):
        if opt.cp: print "CP_DET_MYTORP"
        return struct.pack(self.format, self.code, tnum)

class CP_COPILOT(CP):
    code = 22
    format = '!bbxx'

    def data(self, state=1):
        if opt.cp: print "CP_COPILOT"
        return struct.pack(self.format, self.code, state)

class CP_REFIT(CP):
    code = 23
    format = '!bbxx'

    def data(self, ship):
        if opt.cp: print "CP_REFIT ship=",ship
        return struct.pack(self.format, self.code, ship)

class CP_TRACTOR(CP):
    code = 24
    format = '!bbbx'

    def data(self, state, pnum):
        if opt.cp: print "CP_TRACTOR state=",state,"pnum=",pnum
        return struct.pack(self.format, self.code, state, pnum)

class CP_REPRESS(CP):
    code = 25
    format = '!bbbx'

    def data(self, state, pnum):
        if opt.cp: print "CP_REPRESS state=",state,"pnum=",pnum
        return struct.pack(self.format, self.code, state, pnum)

class CP_COUP(CP):
    code = 26
    format = '!bxxx'

    def data(self):
        if opt.cp: print "CP_COUP"
        return struct.pack(self.format, self.code)

class CP_OPTIONS(CP):
    code = 28
    format = "!bxxxI96s"

    def data(self, flags, keymap):
        if opt.cp: print "CP_OPTIONS flags=",flags,"keymap=",keymap
        return struct.pack(self.format, self.code, flags, keymap)

class CP_DOCKPERM(CP):
    code = 30
    format = '!bbxx'

    def data(self, state):
        if opt.cp: print "CP_DOCKPERM state=",state
        return struct.pack(self.format, self.code, state)

class CP_RESETSTATS(CP):
    code = 32
    format = '!bbxx'

    def data(self, verify):
        if opt.cp: print "CP_RESETSTATS verify=",verify
        return struct.pack(self.format, self.code, verify)

class CP_RESERVED(CP):
    code = 33
    format = "!bxxx16s16s" 

    def data(self, data, resp):
        if opt.cp: print "CP_RESERVED"
        return struct.pack(self.format, self.code, data, resp)

class CP_SCAN(CP):
    code = 34
    format = '!bbxx'

    def data(self, pnum):
        if opt.cp: print "CP_SCAN pnum=",pnum
        return struct.pack(self.format, self.code, pnum)

class CP_UDP_REQ(CP):
    code = 35
    format = '!bbbxi'

    def data(self, request, connmode, port):
        if opt.cp: print "CP_UDP_REQ request=%d connmode=%d port=%d" % (request, connmode, port)
        return struct.pack(self.format, self.code, request, connmode, port)

class CP_FEATURE(CP):
    code = 60
    format = "!bcbbi80s"

    def data(self, type, arg1, arg2, value, name):
        if opt.cp: print "CP_FEATURE type=",type,"arg1=",arg1,"arg2=",arg2,"value=",value,"name=",name
        return struct.pack(self.format, self.code, type, arg1, arg2, value, name)

class CP_PING_RESPONSE(CP):
    code = 42
    format = "!bBbxll"

    def data(self, number, pingme, cp_sent, cp_recv):
        if opt.cp: print "CP_PING_RESPONSE pingme=", pingme
        return struct.pack(self.format, self.code, number, pingme, cp_sent, cp_recv)

""" server originated packets
"""

sp_table = {}

class ServerPacket(type):
    def __new__(cls, name, bases, dct):
        server_packet = type.__new__(cls, name, bases, dct)

        if dct['code'] not in sp_table:
            obj = server_packet()
            sp_table[server_packet.code] = (
                struct.calcsize(server_packet.format), obj)
            if name.lower() not in globals():
                globals()[name.lower()] = obj

        return server_packet

class SP:
    __metaclass__ = ServerPacket
    code = -1
    format = ''

    def find(self, number):
        """ given a packet type return a tuple consisting of
            (size, instance), or (1, self) if type not known
        """
        if not sp_table.has_key(number):
            return (1, self)
        return sp_table[number]

    def handler(self, data):
        raise NotImplemented


class SP_MOTD(SP):
    code = 11
    format = '!bxxx80s'

    def handler(self, data):
        (ignored, message) = struct.unpack(self.format, data)
        message = strnul(message)
        if opt.sp: print "SP_MOTD message=", message
        galaxy.motd.add(message)

class SP_YOU(SP):
    code = 12
    format = '!bbbbbbxxIlllhhhh'

    def handler(self, data):
        global opt
        (ignored, pnum, hostile, swar, armies, tractor, flags, damage,
         shield, fuel, etemp, wtemp, whydead, whodead) = struct.unpack(self.format, data)
        if opt.sp: print "SP_YOU pnum=",pnum,"hostile=",team_decode(hostile),"swar=",team_decode(swar),"armies=",armies,"tractor=",tractor,"flags=",flags,"damage=",damage,"shield=",shield,"fuel=",fuel,"etemp=",etemp,"wtemp=",wtemp,"whydead=",whydead,"whodead=",whodead
        ship = galaxy.ship(pnum)
        ship.sp_you(hostile, swar, armies, tractor, flags, damage, shield, fuel, etemp, wtemp, whydead, whodead)
        if nt.mode == COMM_TCP and ship.speed == 0:
            galaxy.torp_aging()
        if opt.name:
            nt.send(cp_updates.data(1000000/opt.updates))
            nt.send(cp_login.data(0, opt.name, opt.password, opt.login))
            opt.name = None

class SP_QUEUE(SP):
    code = 13
    format = '!bxh'

    def handler(self, data):
        (ignored, pos) = struct.unpack(self.format, data)
        if opt.sp: print "SP_QUEUE pos=",pos
        # FIXME: present on pygame screen

class SP_PL_LOGIN(SP):
    code = 24
    format = "!bbbx16s16s16s" 

    def handler(self, data):
        (ignored, pnum, rank, name, monitor,
         login) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PL_LOGIN pnum=",pnum,"rank=",rank,"name=",strnul(name),"monitor=",strnul(monitor),"login=",strnul(login)
        ship = galaxy.ship(pnum)
        ship.sp_pl_login(rank, name, monitor, login)

class SP_HOSTILE(SP):
    code = 22
    format = "!bbbb"

    def handler(self, data):
        (ignored, pnum, war, hostile) = struct.unpack(self.format, data)
        if opt.sp: print "SP_HOSTILE pnum=",pnum,"war=",team_decode(war),"hostile=",team_decode(hostile)
        ship = galaxy.ship(pnum)
        ship.sp_hostile(war, hostile)

class SP_PLAYER_INFO(SP):
    code = 2
    format = "!bbbb"

    def handler(self, data):
        (ignored, pnum, shiptype, team) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLAYER_INFO pnum=",pnum,"shiptype=",shiptype,"team=",team_decode(team)
        ship = galaxy.ship(pnum)
        ship.sp_player_info(shiptype, team)

class SP_KILLS(SP):
    code = 3
    format = "!bbxxI"

    def handler(self, data):
        (ignored, pnum, kills) = struct.unpack(self.format, data)
        if opt.sp: print "SP_KILLS pnum=",pnum,"kills=",kills
        ship = galaxy.ship(pnum)
        ship.sp_kills(kills)

class SP_PSTATUS(SP):
    code = 20
    format = "!bbbx"

    def handler(self, data):
        (ignored, pnum, status) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PSTATUS pnum=",pnum,"status=",status
        ship = galaxy.ship(pnum)
        ship.sp_pstatus(status)

class SP_PLAYER(SP):
    code = 4
    format = "!bbBbll"

    def handler(self, data):
        (ignored, pnum, dir, speed, x, y) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLAYER pnum=",pnum,"dir=",dir,"speed=",speed,"x=",x,"y=",y
        ship = galaxy.ship(pnum)
        ship.sp_player(dir, speed, x, y)
        if nt.mode == COMM_TCP and ship == me:
            galaxy.torp_aging()

class SP_FLAGS(SP):
    code = 18
    format = "!bbbxI"

    def handler(self, data):
        (ignored, pnum, tractor, flags) = struct.unpack(self.format, data)
        if opt.sp: print "SP_FLAGS pnum=",pnum,"tractor=",tractor,"flags=",flags
        ship = galaxy.ship(pnum)
        ship.sp_flags(tractor, flags)

class SP_PLANET_LOC(SP):
    code = 26
    format = "!bbxxll16s" 

    def handler(self, data):
        (ignored, pnum, x, y, name) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLANET_LOC pnum=",pnum,"x=",x,"y=",y,"name=",strnul(name)
        planet = galaxy.planet(pnum)
        planet.sp_planet_loc(x, y, name)

class SP_LOGIN(SP):
    code = 17
    format = "!bbxxl96s"
    callback = None

    def uncatch(self):
        self.callback = None

    def catch(self, callback):
        self.callback = callback

    def handler(self, data):
        (ignored, accept, flags, keymap) = struct.unpack(self.format, data)
        if opt.sp: print "SP_LOGIN accept=",accept,"flags=",flags
        if self.callback:
            self.callback(accept, flags, keymap)
            self.uncatch()
        if accept == 1:
            nt.send(cp_ping_response.data(0, 1, 0, 0))

class SP_MASK(SP):
    code = 19
    format = "!bbxx"
    callback = None

    def uncatch(self):
        self.callback = None

    def catch(self, callback):
        self.callback = callback

    def handler(self, data):
        (ignored, mask) = struct.unpack(self.format, data)
        if opt.sp: print "SP_MASK mask=",team_decode(mask)
        if self.callback:
            self.callback(mask)
        # FIXME: #1187683470 update team selection icons in response to SP_MASK

class SP_PICKOK(SP):
    code = 16
    format = "!bbxx"
    callback = None

    def uncatch(self):
        self.callback = None

    def catch(self, callback):
        self.callback = callback

    def handler(self, data):
        (ignored, state) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PICKOK state=",state
        nt.sp_pickok()
        if self.callback:
            self.callback(state)
            self.uncatch()

class SP_RESERVED(SP):
    code = 25
    format = "!bxxx16s"

    def handler(self, data):
        (ignored, data) = struct.unpack(self.format, data)
        text = struct.unpack('16b', data)
        if opt.sp: print "SP_RESERVED data=",text
        resp = data
        # FIXME: generate correct response data
        nt.send(cp_reserved.data(data, resp))

class SP_TORP_INFO(SP):
    code = 5
    format = "!bbbxhxx"

    def handler(self, data):
        (ignored, war, status, tnum) = struct.unpack(self.format, data)
        if opt.sp: print "SP_TORP_INFO war=%s status=%d tnum=%d" % (str(team_decode(war)), status, tnum)
        torp = galaxy.torp(tnum)
        torp.sp_torp_info(war, status)

class SP_TORP(SP):
    code = 6
    format = "!bBhll"

    def handler(self, data):
        (ignored, dir, tnum, x, y) = struct.unpack(self.format, data)
        if opt.sp: print "SP_TORP dir=%d tnum=%d x=%d y=%d" % (dir, tnum, x, y)
        torp = galaxy.torp(tnum)
        torp.sp_torp(dir, x, y)

class SP_PLASMA_INFO(SP):
    code = 8
    format = "!bbbxhxx"

    def handler(self, data):
        (ignored, war, status, pnum) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLASMA_INFO war=",team_decode(war),"status=",status,"pnum=",pnum
        plasma = galaxy.plasma(pnum)
        plasma.sp_plasma_info(war, status)

class SP_PLASMA(SP):
    code = 9
    format = "!bxhll"

    def handler(self, data):
        (ignored, pnum, x, y) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLASMA pnum=",pnum,"x=",x,"y=",y
        plasma = galaxy.plasma(pnum)
        plasma.sp_plasma(x, y)

class SP_STATUS(SP):
    code = 14
    format = "!bbxxIIIIIL"

    def handler(self, data):
        (ignored, tourn, armsbomb, planets, kills, losses, time, timeprod) = struct.unpack(self.format, data)
        if opt.sp: print "SP_STATUS tourn=",tourn,"armsbomb=",armsbomb,"planets=",planets,"kills=",kills,"losses=",losses,"time=",time,"timepro=",timeprod
        # FIXME: display t-mode state, and hey, the other things might be fun

class SP_PHASER(SP):
    code = 7
    format = "!bbbBlll" 

    def handler(self, data):
        (ignored, pnum, status, dir, x, y, target) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PHASER pnum=",pnum,"status=",status,"dir=",dir,"x=",x,"y=",y,"target=",target
        phaser = galaxy.phaser(pnum)
        phaser.sp_phaser(status, dir, x, y, target)

class SP_PLANET(SP):
    code = 15
    format = "!bbbbhxxl" 

    def handler(self, data):
        (ignored, pnum, owner, info, flags, armies) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PLANET pnum=",pnum,"owner=",owner,"info=",info,"flags=",flags,"armies=",armies
        planet = galaxy.planet(pnum)
        planet.sp_planet(owner, info, flags, armies)

class SP_MESSAGE(SP):
    code = 1
    format = "!bBBB80s"

    def handler(self, data):
        (ignored, m_flags, m_recpt, m_from, mesg) = struct.unpack(self.format, data)
        if opt.sp: print "SP_MESSAGE m_flags=",m_flags,"m_recpt=",m_recpt,"m_from=",m_from,"mesg=",strnul(mesg)
        galaxy.sp_message(m_flags, m_recpt, m_from, mesg)

class SP_STATS(SP):
    code = 23
    format = "!bbxx13l"

    def handler(self, data):
        (ignored, pnum, tkills, tlosses, kills, losses, tticks, tplanets, tarmies, sbkills, sblosses, armies, planets, maxkills, sbmaxkills) = struct.unpack(self.format, data)
        if opt.sp: print "SP_STATS pnum=",pnum,"tkills=",tkills,"tlosses=",tlosses,"kills=",kills,"losses=",losses,"tticks=",tticks,"tplanets=",tplanets,"tarmies=",tarmies,"sbkills=",sbkills,"sblosses=",sblosses,"armies=",armies,"planets=",planets,"maxkills=",maxkills,"sbmaxkills=",sbmaxkills

class SP_WARNING(SP):
    code = 10
    format = '!bxxx80s'
    text = ''
    seen = False

    def handler(self, data):
        (ignored, message) = struct.unpack(self.format, data)
        if opt.sp: print "SP_WARNING message=", strnul(message)
        self.text = strnul(message)
        self.seen = False

class SP_FEATURE(SP):
    code = 60
    format = "!bcbbi80s"

    def handler(self, data):
        (ignored, type, arg1, arg2, value, name) = struct.unpack(self.format, data)
        name = strnul(name)
        if opt.sp:
            print "SP_FEATURE type=%s arg1=%d arg2=%d value=%d name=%s" % (type, arg1, arg2, value, name)
        if (type, arg1, arg2, value, name) == ('S', 0, 0, 1, 'FEATURE_PACKETS'):
            # server says features packets are okay to send,
            # so send this client's features
            if rcd.cp_feature: # we want binary RCDs in SP_MESSAGE packets
                nt.send(cp_feature.data('S', 0, 0, 1, 'RC_DISTRESS'))
            nt.send(cp_feature.data('S', 0, 0, 1, 'SHIP_CAP'))

        if name == 'UPS':
            galaxy.ups = value
        # FIXME: process the other feature packets received

class SP_BADVERSION(SP):
    code = 21
    format = "!bbxx"
    why = None

    def handler(self, data):
        (ignored, why) = struct.unpack(self.format, data)
        self.why = why

class SP_PING(SP):
    """ only received if client sends CP_PING_RESPONSE after SP_LOGIN """
    code = 46
    format = "!bBHBBBB" 

    def handler(self, data):
        (ignored, number, lag, tloss_sc, tloss_cs, iloss_sc, iloss_cs) = struct.unpack(self.format, data)
        if opt.sp: print "SP_PING"
        nt.send(cp_ping_response.data(0, 1, 0, 0))

class SP_UDP_REPLY(SP):
    """ only received if client sends CP_UDP_REQ """
    code = 28
    format = "!bbxxi" 

    def handler(self, data):
        (ignored, reply, port) = struct.unpack(self.format, data)
        if opt.sp: print "SP_UDP_REPLY reply=%d port=%d" % (reply, port)
        nt.sp_udp_reply(reply, port)

class SP_SEQUENCE(SP):
    """ only received if client sends CP_UDP_REQ requesting COMM_UDP """
    code = 29
    format = "!bBH" 

    def handler(self, data):
        (ignored, flag, sequence) = struct.unpack(self.format, data)
        galaxy.torp_aging()
        if opt.sp: print "SP_SEQUENCE flag=%d sequence=%d" % (flag, sequence)

class SP_SHIP_CAP(SP):
    """ only received if client sends CP_FEATURE feature packet SHIP_CAP """
    code = 39
    format = "!bbHHHiiiiiiHHH1sx16s2sH"

    def handler(self, data):
        (ignored, operation, s_type, s_torpspeed, s_phaserrange, s_maxspeed, s_maxfuel, s_maxshield, s_maxdamage, s_maxwpntemp, s_maxegntemp, s_width, s_height, s_maxarmies, s_letter, s_name, s_desig, s_bitmap) = struct.unpack(self.format, data)
        if opt.sp: print "SP_SHIP_CAP operation=%d s_type=%d s_torpspeed=%d s_phaserrange=%d s_maxspeed=%d s_maxfuel=%d s_maxshield=%d s_maxdamage=%d s_maxwpntemp=%d s_maxegntemp=%d s_width=%d s_height=%d s_maxarmies=%d s_letter=%s s_name=%s s_desig=%s s_bitmap=%d" % (operation, s_type, s_torpspeed, s_phaserrange, s_maxspeed, s_maxfuel, s_maxshield, s_maxdamage, s_maxwpntemp, s_maxegntemp, s_width, s_height, s_maxarmies, s_letter, s_name, s_desig, s_bitmap)
        try:
            cap = galaxy.cap(s_type)
        except:
            print "SP_SHIP_CAP s_type was invalid: %d" % s_type
            return
        # check operation, zero add or change, one remove
        if operation == 1:
            cap.reset(s_type)
            return
        if operation != 0:
            print "SP_SHIP_CAP operation was invalid: %d" % operation
            return
        cap.seen = False
        cap.s_torpspeed = s_torpspeed
        cap.s_phaserrange = s_phaserrange
        cap.s_maxspeed = s_maxspeed
        cap.s_maxfuel = s_maxfuel
        cap.s_maxshield = s_maxshield
        cap.s_maxdamage = s_maxdamage
        cap.s_maxwpntemp = s_maxwpntemp
        cap.s_maxegntemp = s_maxegntemp
        cap.s_width = s_width
        cap.s_height = s_height
        cap.s_maxarmies = s_maxarmies
        cap.s_letter = s_letter
        cap.s_name = s_name
        cap.s_desig = s_desig
        cap.s_bitmap = s_bitmap

""" user interface display phases
"""

class Phase:
    """ display phases common code """
    def __init__(self):
        self.warn_on = False
        self.warn_fuse = 0
        self.ue_hz = 10
        self.ue_delay = 1000 / self.ue_hz
        self.screenshot = 0
        self.run = False
        self.eh_md = [] # event handlers, mouse down
        self.eh_mu = [] # event handlers, mouse up
        self.eh_ue = [] # event handlers, user events (timers)

    def button(self, clicked, text, x, y, size, colour):
        b = Button(clicked, text, x, y, size, colour)
        self.eh_md.append(b.md)
        self.eh_mu.append(b.mu)
        b.draw()
        return b

    def add_quit_button(self, clicked):
        self.b_quit = self.button(clicked, 'QUIT', 900, 950, 32, colour=(255, 255, 255))

    def add_list_button(self, clicked):
        self.b_list = self.button(clicked, 'LIST', 20, 950, 32, colour=(255, 255, 255))

    def warn(self, message, ms=0):
        font = fc.get('DejaVuSans.ttf', 32)
        text = font.render(message, 1, (255, 127, 127))
        self.warn_br = text.get_rect(center=(screen.get_width()/2,
                                             screen.get_height()-90))
        self.warn_bg = screen.subsurface(self.warn_br).copy()
        r1 = screen.blit(text, self.warn_br)
        pygame.display.update(r1)
        self.warn_on = True
        self.warn_fuse = ms / self.ue_delay

    def unwarn(self):
        if self.warn_on:
            r1 = screen.blit(self.warn_bg, self.warn_br)
            pygame.display.update(r1)
            self.warn_on = False

    def warn_ue(self):
        if self.warn_fuse > 0:
            self.warn_fuse = self.warn_fuse - 1
            if self.warn_fuse == 0:
                self.unwarn()
        
    def background(self, name="stars.png"):
        # tile a background image onto the screen
        screen.fill((0,0,0))
        if opt.no_backgrounds: return
        # IMAGERY: stars.png
        background = ic.get(name)
        bh = background.get_height()
        bw = background.get_width()
        for y in range(screen.get_height() / bh + 1):
            for x in range(screen.get_width() / bw + 1):
                screen.blit(background, (x*bw, y*bh))

    def text(self, text, x, y, size=72, colour=(255, 255, 255)):
        font = fc.get('DejaVuSans.ttf', size)
        ts = font.render(text, 1, colour)
        tr = ts.get_rect(center=(x, y))
        screen.blit(ts, tr)

    def blame(self):
        self.text("software by quozl@us.netrek.org and stephen@thorne.id.au", screen.get_width()/2, screen.get_height()-30, 16)
        more = ""
        if not opt.no_backgrounds: more = "backgrounds by hubble, "
        self.text(more + "ships by pascal", screen.get_width()/2, screen.get_height()-15, 16)
        
    def welcome(self):
        global WELCOME

        font = fc.get('DejaVuSansMono.ttf', 14)
        x = 200
        y = 790
        for line in WELCOME:
            ts = font.render(line, 1, (255, 255, 255))
            tr = ts.get_rect(left=x, top=y)
            y = tr.bottom
            screen.blit(ts, tr)

    def network_sink(self):
        return nt.recv()
        
    def display_sink_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.md(event)
        elif event.type == pygame.KEYDOWN:
            self.kb(event)
        elif event.type == pygame.QUIT:
            nt.send(cp_bye.data())
            # FIXME: exit main instead of calling sys.exit
            sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            self.mm(event)
        elif event.type > pygame.USEREVENT:
            self.ue(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mu(event)
        
    def display_sink(self):
        for event in pygame.event.get():
            self.display_sink_event(event)

    def display_sink_wait(self):
        event = pygame.event.wait()
        self.display_sink_event(event)

    def ue(self, event):
        for eh in self.eh_ue:
            if eh(event): return True
        return False

    def ue_set(self, hz):
        self.ue_hz = hz
        self.ue_delay = 1000 / hz
        pygame.time.set_timer(pygame.USEREVENT+1, self.ue_delay)

    def ue_clear(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 0)
        
    def mm(self, event):
        # FIXME: watch for MOUSEMOTION and update object information panes
        # for planets or ships (on tactical or galactic)
        pass

    def md(self, event):
        for eh in self.eh_md:
            if eh(event): return True
        return False

    def mu(self, event):
        for eh in self.eh_mu:
            if eh(event): return True
        return False

    def kb(self, event):
        if event.key == pygame.K_q:
            self.quit(event)
        elif event.key == pygame.K_ESCAPE:
            self.snap(event)

    def exit(self, status):
        screen.fill((0, 0, 0))
        pygame.display.flip()
        ic.statistics()
        pg_quit()
        # FIXME: exit main instead of calling sys.exit
        sys.exit(status)

    def quit(self, event):
        if nt.mode != None:
            nt.send(cp_quit.data())
        else:
            self.exit(0)

    def snap(self, event):
        pygame.image.save(screen, "netrek-client-pygame-%04d.tga" % self.screenshot)
        print "snapshot taken"
        self.screenshot += 1

    def cycle(self):
        """ free wheeling cycle, use when it is acceptable to block on
        either display or network events, without local user event
        timers (a timer scheduled in this mode will not fire until
        after a display or network event occurs) """
        while self.run:
            self.network_sink()
            self.display_sink()
    
    def cycle_wait(self):
        """ display waiting cycle, use when local user event timers
        are needed """
        while self.run:
            self.network_sink()
            self.display_sink_wait()
    
    def cycle_wait_display(self):
        """ display waiting cycle, use when local user event timers
        are needed, and no network events """
        while self.run:
            self.display_sink_wait()
    
class PhaseSplash(Phase):
    """ splash screen, shows welcome for a short time, and the player
    is to either wait for the timer to expire, or click to cancel """
    def __init__(self, screen):
        Phase.__init__(self)
        self.background("hubble-helix.jpg")
        x = screen.get_width()/2
        y = screen.get_height()/2
        self.text("netrek", x, y, 144)
        self.bouncer = Bouncer(200, 200, x, y, 'torp-explode-20.png', 'torp-explode-20.png')
        self.welcome()
        self.add_quit_button(self.quit)
        pygame.display.flip()
        if opt.screenshots:
            pygame.image.save(screen, "netrek-client-pygame-splash.tga")
        self.ue_set(100)
        self.fuse_was = self.fuse = opt.splashtime / self.ue_delay
        self.run = True
        self.cycle_wait_display() # returns after self.leave is called
        self.ue_clear()

    def ue(self, event):
        self.fuse -= 1
        if self.fuse < 0:
            self.leave()
        else:
            self.bouncer.update(self.fuse, self.fuse_was)

    def md(self, event):
        if Phase.md(self, event): return
        self.leave()

    def kb(self, event):
        self.leave()

    def leave(self):
        self.b_quit.clear()
        pygame.display.flip()
        self.run = False

class PhaseServers(Phase):
    """ metaserver list, a list of services is shown, the list is
    derived from the metaserver and multicast discovery, and the
    player is to either select one with mouse, wait for the list to
    update, or quit. """
    def __init__(self, screen, mc):
        Phase.__init__(self)
        self.background("hubble-orion.jpg")
        x = screen.get_width()/2
        self.text('netrek', x, 100, 92)
        self.text('server list', x, 175, 64)
        self.welcome()
        self.add_quit_button(self.quit)
        pygame.display.flip()
        self.bouncer = Bouncer(225, 20, x, 240)
        self.dy = 40 # vertical spacing
        self.n = 0 # number of servers shown so far
        self.run = True
        self.mc = mc
        self.mc.uncork(self.update)
        self.timing = False
        self.sent = pygame.time.get_ticks()
        self.lag = 0
        self.ue_set(100)
        self.fuse_was = opt.metaserver_refresh_interval * 1000 / self.ue_delay
        self.fuse = self.fuse_was / 2
        self.cycle_wait() # returns after self.leave is called
        self.ue_clear()

    def server_icon(self, y):
        # IMAGERY: servers-icon.png
        return Icon('servers-icon.png', 70, y)

    def server_name(self, y, server):
        """ server name, shade by age """
        colour = 64
        age = server['age']
        if age < 3000: colour = 128
        if age < 300: colour = 192
        if age < 180: colour = 255
        colour = (colour, colour, colour)
        return Text(server['name'] + ' ' + server['comment'], 100, y, 22, colour)

    def server_queue(self, y, server):
        return Text('Q' + str(server['queue']), 500, y, 22, (255, 0, 0))

    def server_players(self, y, server):
        s = []
        # per player icon
        gx = 500
        for x in range(min(server['players'], 16)):
            # per player icon
            # IMAGERY: servers-player.png
            s.append(Icon('servers-player.png', gx, y))
            # space them out for visual counting
            if (x % 4) == 3:
                gx = gx + 35
            else:
                gx = gx + 30
        return s

    def update(self, name):
        """ called by MetaClient for each server for which a packet is received
        """
        # FIXME: seen once, placement problem, a newly available
        # multicast server is placed at first position despite first
        # position being taken already by a metaserver entry.
        # FIXME: old multicast entries not expired when they leave.
        redraw = []
        server = self.mc.servers[name]
        if self.timing and server['source'] == 'r':
            self.lag = pygame.time.get_ticks() - self.sent
            self.warn('ping ' + str(self.lag) + 'ms', 1500)
            self.timing = False
        if not server.has_key('y'):
            y = 300 + self.dy * self.n
            self.n += 1
        else:
            y = server['y']
            for sprite in server['sprites']:
                redraw.append(sprite.clear())
        sprites = []
        sprites.append(self.server_icon(y))
        sprites.append(self.server_name(y, server))
        if server['queue'] > 0:
            sprites.append(self.server_queue(y, server))
        else:
            sprites += self.server_players(y, server)
        self.mc.servers[name]['y'] = y
        self.mc.servers[name]['sprites'] = sprites
        
        for sprite in sprites:
            redraw.append(sprite.draw())
        pygame.display.update(redraw)
    
    def network_sink(self):
        self.mc.recv()

    def ue(self, event):
        self.warn_ue()
        self.bouncer.update(self.fuse, self.fuse_was)

        self.fuse -= 1
        if self.fuse < 0:
            self.sent = pygame.time.get_ticks()
            self.timing = True
            self.mc.query(opt.metaserver)
            self.fuse = self.fuse_was

    def md(self, event):
        if Phase.md(self, event): return
        self.unwarn()
        if event.button != 1:
            self.warn('not that button, mate', 500)
            return
        y = event.pos[1]
        if abs(self.bouncer.cy - y) < 50:
            self.warn('that is the metaserver query refresh timer, mate', 2000)
            return
        distance = self.dy
        chosen = None
        for k, v in self.mc.servers.iteritems():
            dy = abs(v['y'] - y)
            if dy < distance:
                distance = dy
                chosen = v['name']
        if chosen == None:
            self.warn('click on a server, mate', 1000)
            return
        if opt.screenshots:
            pygame.image.save(screen, "netrek-client-pygame-servers.tga")
        pygame.display.update(self.b_quit.clear())
        self.warn('connecting, standby')
        opt.chosen = chosen
        # FIXME: do not block and hang during connect, do it asynchronously
        if not nt.connect(opt.chosen, opt.port):
            # FIXME: handle connection failure more gracefully by
            # explaining what went wrong, rather than be this obtuse
            self.unwarn()
            self.warn('connection failure', 2000)
            pygame.display.update(self.b_quit.draw())
            return
        self.leave()

    def leave(self):
        pygame.display.update(self.b_quit.clear())
        self.run = False

class PhaseLogin(Phase):
    """ login, the server message of the day (MOTD) is displayed, and
    the player is to type a character name and password, the name may
    be guest, or the player may quit. """
    def __init__(self, screen):
        Phase.__init__(self)
        self.background("hubble-crab.jpg")
        x = screen.get_width()/2
        self.text('netrek', x, 100, 92)
        self.text(opt.chosen, x, 185, 64)
        self.blame()
        self.warn('connected, waiting for slot, standby')
        pygame.display.flip()
        # pause until SP_YOU is received, which marks end of SP_MOTD
        # (while on queue, this pauses)
        while me == None:
            nt.recv()
            # FIXME: allow QUIT here
        self.add_quit_button(self.quit)
        self.add_list_button(self.list)
        self.unwarn()
        self.warn('connected, as slot %s, ready to login' % slot_decode(me.n))
        self.texts = Texts(galaxy.motd.get(), 100, 250, 24, 16)
        pygame.display.flip()
        self.name = Field("type a name ? ", "", x, 750)
        self.focused = self.name
        self.password = None
        self.run = True
        if opt.screenshots:
            pygame.image.save(screen, "netrek-client-pygame-login.tga")
        self.cancelled = False
        self.cycle() # returns when login is complete, or cancelled

    def tab(self):
        # FIXME: just press enter for guest
        """ move to next field """
        self.focused.leave()
        if self.focused == self.password:
            self.chuck_cp_login()
        elif self.focused == self.name:
            if self.password == None:
                self.password = Field("password ? ", "", 500, 800)
                # FIXME: password prompt appears momentarily if guest selected
                # FIXME: #1187683521 force no echo for password
            else:
                self.password.enter()
            self.focused = self.password
            if self.name.value == 'guest' or self.name.value == 'Guest':
                self.password.leave()
                self.password.undraw()
                self.password.value = ''
                self.chuck_cp_login()
            else:
                self.chuck_cp_login_attempt()

    def chuck_cp_login_attempt(self):
        self.catch_sp_login_attempt()
        nt.send(cp_login.data(1, str(self.name.value), str(self.password.value), 'pynetrek'))

    def throw_sp_login_attempt(self, accept, flags, keymap):
        if accept == 1:
            self.warn('server has this name listed')
        else:
            self.warn('server ignorant of this name')
        
    def catch_sp_login_attempt(self):
        global sp_login
        sp_login.catch(self.throw_sp_login_attempt)

    def chuck_cp_login(self):
        self.catch_sp_login()
        nt.send(cp_updates.data(1000000/opt.updates))
        nt.send(cp_login.data(0, str(self.name.value), str(self.password.value), 'pynetrek'))

    def throw_sp_login(self, accept, flags, keymap):
        if accept == 1:
            self.proceed()
        else:
            self.warn('name and password refused by server')
            self.password.value = ''
            self.password.unhighlight()
            self.focused = self.name
            self.focused.enter()
        
    def catch_sp_login(self):
        global sp_login
        sp_login.catch(self.throw_sp_login)
                
    def untab(self):
        if self.focused == self.password:
            self.focused.leave()
            self.focused = self.name
            self.focused.redraw()

    def kb(self, event):
        self.unwarn()
        shift = (event.mod == pygame.KMOD_SHIFT or
                 event.mod == pygame.KMOD_LSHIFT or
                 event.mod == pygame.KMOD_RSHIFT)
        control = (event.mod == pygame.KMOD_CTRL or
                   event.mod == pygame.KMOD_LCTRL or
                   event.mod == pygame.KMOD_RCTRL)
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: pass
        elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL: pass
        elif event.key == pygame.K_d and control:
            self.list(event)
        elif event.key == pygame.K_w and control:
            self.focused.delete()
        elif event.key == pygame.K_TAB and shift:
            self.untab()
        elif event.key == pygame.K_TAB or event.key == pygame.K_RETURN:
            self.tab()
        elif event.key == pygame.K_BACKSPACE:
            self.focused.backspace()
        elif event.key > 31 and event.key < 255 and not control:
            self.focused.append(event.unicode)
        else:
            return Phase.kb(self, event)
        
    def list(self, event):
        self.cancelled = True
        nt.send(cp_bye.data())
        nt.shutdown()
        self.proceed()

    def quit(self, event):
        self.list(event)
        Phase.quit(self, event)

    def proceed(self):
        self.b_quit.clear()
        self.b_list.clear()
        pygame.display.flip()
        self.run = False

class PhaseOutfit(Phase):
    """ team and ship selection, the available teams and ships are
    displayed, and the player may select one, or quit """
    # FIXME: automatic quit timeout display
    # FIXME: add a become observer button that disconnects, reconnects, using same login credentials
    # FIXME: add a become player button as above
    # FIXME: add a relinquish slot button, for rejoining end of queue
    # FIXME: add a BACK button that disconnects, reconnects, for login
    def __init__(self, screen):
        Phase.__init__(self)
        self.run = True
        self.box = None
        self.last_team = None
        self.last_ship = CRUISER
        self.cancelled = False
        self.visible = pygame.sprite.OrderedUpdates(())
        self.angle = 0
        
    def do(self):
        self.run = True
        self.background("hubble-spire.jpg")
        x = screen.get_width()/2
        self.text('netrek', x, 100, 92)
        self.text(opt.chosen, x, 185, 64)
        self.text('ship and race', x, 255, 64)
        self.blame()
        self.add_quit_button(self.quit)
        self.add_list_button(self.list)
        pygame.display.flip()
        box_l = 212
        box_t = 300
        box_r = 788
        box_b = 875
        r = []
        self.sprites = []
        # FIXME: display number of players on each team
        # FIXME: make these sprites rather than paint on screen
        table = [[FED, -1, +1], [ROM, -1, -1], [KLI, +1, -1], [ORI, +1, +1]]
        for row in table:
            (team, dx, dy) = row
            # box centre
            # FIXME: slide ships into race on race positions, omitting other races
            x = (box_r - box_l) / 2 + box_l
            y = (box_b - box_t) / 2 + box_t
            for ship in [CRUISER, ASSAULT, SCOUT, BATTLESHIP, DESTROYER, STARBASE]:
                x = x + dx * 60
                y = y + dy * 60
                # IMAGERY: ???-??.png
                sprite = RotatingIcon(teams[team]+'-'+ships[ship]+'.png', x, y, self.angle)
                sprite.description = teams_long[team] + ' ' + ships_long[ship] + ', ' + ships_use[ship]
                sprite.x = x
                sprite.y = y
                sprite.ship = ship
                sprite.team = team
                sprite.visible = False
                sprite.suck()
                self.sprites.append(sprite)
        # FIXME: add minature galactic, showing ownership, player
        # positions if any, with ships to choose in each race space or
        # just outside the corner.
        # FIXME: display "in bronco you should remain with your team"
        # FIXME: show logged in players
        # FIXME: show planet status
        # FIXME: show whydead
        self.warn("in netrek all races are equal")
        pygame.display.update(r)
        sp_mask.catch(self.mask)
        if opt.screenshots:
            pygame.image.save(screen, "netrek-client-pygame-outfit.tga")
        self.auto()
        self.cycle() # returns when choice accepted by server, or user cancels
        sp_mask.uncatch()

    def mask(self, mask):
        r = []
        for sprite in self.sprites:
            if mask & sprite.team:
                if not sprite.visible:
                    self.visible.add(sprite)
                    r.append(sprite.blit())
                    sprite.visible = True
            else:
                if sprite.visible:
                    self.visible.remote(sprite)
                    r.append(sprite.clear())
                    sprite.visible = False
        if len(r) > 0:
            pygame.display.update(r)
        # FIXME: display SP_WARNING packets (confirm team change)
        # using WarningSprite

    def auto(self):
        # attempt auto-refit if command line arguments are supplied
        # FIXME: this appears to be persistent, even if we quit
        if opt.team != None and opt.ship != None:
            while me == None:
                nt.recv()
            for team, name in teams_long.iteritems():
                if opt.team == name[:len(opt.team)]:
                    for ship, name in ships.iteritems():
                        if opt.ship == name[:len(opt.ship)]:
                            self.team(teams_numeric[team], ship)
                            break
                    break

    def team(self, team, ship):
        self.last_team = team
        self.last_ship = ship
        sp_pickok.catch(self.sp_pickok)
        nt.send(cp_outfit.data(team, ship))

    def sp_pickok(self, state):
        if state == 1:
            self.run = False
        else:
            self.unwarn()
            self.warn('outfit request refused by server')

    def nearest(self, pos):
        (x, y) = pos
        nearest = None
        minimum = 70**2
        for sprite in self.sprites:
            if not sprite.visible: continue
            distance = (sprite.x - x)**2 + (sprite.y - y)**2
            if distance < minimum:
                nearest = sprite
                minimum = distance
        return nearest

    def md(self, event):
        if Phase.md(self, event): return
        self.unwarn()
        nearest = self.nearest(event.pos)
        if nearest != None:
            self.team(teams_numeric[nearest.team], nearest.ship)
        else:
            self.warn('click on a ship, mate')
        # FIXME: click on team icon sends CP_OUTFIT most recent ship
        # FIXME: click on ship icon requests CP_OUTFIT with team and ship
        
    def mm(self, event):
        nearest = self.nearest(event.pos)
        if nearest != self.box:
            self.unwarn()
            if nearest != None:
                self.warn(nearest.description)
            self.box = nearest
        
    def kb(self, event):
        self.unwarn()
        shift = (event.mod == pygame.KMOD_SHIFT or
                 event.mod == pygame.KMOD_LSHIFT or
                 event.mod == pygame.KMOD_RSHIFT)
        control = (event.mod == pygame.KMOD_CTRL or
                   event.mod == pygame.KMOD_LCTRL or
                   event.mod == pygame.KMOD_RCTRL)
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: pass
        elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL: pass
        elif event.key == pygame.K_d and control:
            self.list(event)
        elif event.key == pygame.K_q:
            self.quit(event)
        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            if self.last_team != None:
                self.team(self.last_team, self.last_ship)
        elif event.key == pygame.K_f: self.team(0, self.last_ship)
        elif event.key == pygame.K_r: self.team(1, self.last_ship)
        elif event.key == pygame.K_k: self.team(2, self.last_ship)
        elif event.key == pygame.K_o: self.team(3, self.last_ship)
        else:
            return Phase.kb(self, event)

    def list(self, event):
        nt.send(cp_bye.data())
        nt.shutdown()
        self.cancelled = True
        self.proceed()
        
    def quit(self, event):
        nt.send(cp_bye.data())
        nt.shutdown()
        self.exit(0)

    def proceed(self):
        self.b_quit.clear()
        self.b_list.clear()
        pygame.display.flip()
        self.run = False

class PhaseFlight(Phase):
    def __init__(self, name):
        Phase.__init__(self)
        self.run = True
        self.frames = 0
        self.events = 0
        self.start = time.time()
        self.name = name
        self.set_keys()
        self.eh_ue.append(b_warning_sprite.ue)

    def __del__(self):
        end = time.time()
        elapsed = end - self.start
        fps = self.frames / elapsed
        print "%s: frames=%d elapsed=%d rate=%d events=%d" % (self.name, self.frames, elapsed, fps, self.events)

    def cycle(self):
        """ main in-flight event loop, returns when no longer flying """
        self.update()
        self.frames += 1
        while self.run:
            packets = self.network_sink()
            if not packets:
                self.display_sink()
                self.events += 1
            if packets:
                self.update()
                self.frames += 1
            if me.status == POUTFIT: break # no longer flying

    def update(self):
        raise NotImplemented

    def md(self, event):
        """ mouse button down event handler
        position is a list of (x, y) screen coordinates
        button is a mouse button number
        """
        global me
        if event.button == 3 and me != None:
            (x, y) = event.pos
            nt.send(cp_direction.data(xy_to_dir(x, y)))
        elif event.button == 2 and me != None:
            (x, y) = event.pos
            nt.send(cp_phaser.data(xy_to_dir(x, y)))
        elif event.button == 1 and me != None:
            (x, y) = event.pos
            nt.send(cp_torp.data(xy_to_dir(x, y)))
    
    def kb(self, event):

        # ignore the shift and control keys on their own
        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: return
        if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL: return

        # check for control key sequences pressed
        if (event.mod == pygame.KMOD_CTRL or
            event.mod == pygame.KMOD_LCTRL or
            event.mod == pygame.KMOD_RCTRL):
            if self.keys_control.has_key(event.key):
                (handler, argument) = self.keys_control[event.key]
                handler(event, argument)
                return

        # check for shift key sequences pressed
        if (event.mod == pygame.KMOD_SHIFT or
            event.mod == pygame.KMOD_LSHIFT or
            event.mod == pygame.KMOD_RSHIFT):
            if self.keys_shift.has_key(event.key):
                (handler, argument) = self.keys_shift[event.key]
                handler(event, argument)
                return

        # check for normal keys pressed
        if self.keys_normal.has_key(event.key):
            (handler, argument) = self.keys_normal[event.key]
            handler(event, argument)
            return

        return Phase.kb(self, event)

    def set_keys(self):
        """ define dictionaries to map keys to operations """
        self.keys_normal = {
            pygame.K_0: (self.op_warp, 0),
            pygame.K_1: (self.op_warp, 1),
            pygame.K_2: (self.op_warp, 2),
            pygame.K_3: (self.op_warp, 3),
            pygame.K_4: (self.op_warp, 4),
            pygame.K_5: (self.op_warp, 5),
            pygame.K_6: (self.op_warp, 6),
            pygame.K_7: (self.op_warp, 7),
            pygame.K_8: (self.op_warp, 8),
            pygame.K_9: (self.op_warp, 9),
            pygame.K_SEMICOLON: (self.op_planet_lock, None),
            pygame.K_b: (self.op_bomb, None),
            pygame.K_c: (self.op_cloak_toggle, None),
            pygame.K_d: (self.op_det, None),
            pygame.K_e: (self.op_docking_toggle, None),
            pygame.K_l: (self.op_player_lock, None),
            pygame.K_o: (self.op_orbit, None),
            pygame.K_s: (self.op_shield_toggle, None),
            pygame.K_u: (self.op_shield_toggle, None),
            pygame.K_x: (self.op_beam_down, None),
            pygame.K_y: (self.op_pressor_toggle, None),
            pygame.K_z: (self.op_beam_up, None),
            }
        self.keys_control = {
            pygame.K_HASH: (self.op_distress, rcd.dist_type_other2),
            pygame.K_0: (self.op_distress, rcd.dist_type_pop),
            pygame.K_1: (self.op_distress, rcd.dist_type_save_planet),
            pygame.K_2: (self.op_distress, rcd.dist_type_base_ogg),
            pygame.K_3: (self.op_distress, rcd.dist_type_help1),
            pygame.K_4: (self.op_distress, rcd.dist_type_help2),
            pygame.K_5: (self.op_distress, rcd.dist_type_asw),
            pygame.K_6: (self.op_distress, rcd.dist_type_asbomb),
            pygame.K_7: (self.op_distress, rcd.dist_type_doing1),
            pygame.K_8: (self.op_distress, rcd.dist_type_doing2),
            pygame.K_9: (self.op_distress, rcd.dist_type_pickup),
            pygame.K_AT: (self.op_distress, rcd.dist_type_other1),
            pygame.K_b: (self.op_distress, rcd.dist_type_bomb),
            pygame.K_c: (self.op_distress, rcd.dist_type_space_control),
            pygame.K_e: (self.op_distress, rcd.dist_type_escorting),
            pygame.K_f: (self.op_distress, rcd.dist_type_free_beer),
            pygame.K_h: (self.op_distress, rcd.dist_type_crippled),
            pygame.K_l: (self.op_distress, rcd.dist_type_controlling),
            pygame.K_m: (self.op_distress, rcd.dist_type_bombing),
            pygame.K_n: (self.op_distress, rcd.dist_type_no_gas),
            pygame.K_o: (self.op_distress, rcd.dist_type_ogg),
            pygame.K_p: (self.op_distress, rcd.dist_type_ogging),
            pygame.K_t: (self.op_distress, rcd.dist_type_take),
            }
        self.keys_shift = {
            pygame.K_COMMA: (self.op_warp_down, None),
            pygame.K_PERIOD: (self.op_warp_up, None),
            pygame.K_0: (self.op_warp, 10),
            pygame.K_1: (self.op_warp, 11),
            pygame.K_2: (self.op_warp, 12),
            pygame.K_3: (self.op_warp_half, None),
            pygame.K_4: (self.op_null, None),
            pygame.K_5: (self.op_warp_full, None),
            pygame.K_6: (self.op_null, None),
            pygame.K_7: (self.op_null, None),
            pygame.K_8: (self.op_practice, None),
            pygame.K_9: (self.op_warp, 10),
            pygame.K_d: (self.op_det_me, None),
            pygame.K_e: (self.op_distress, rcd.dist_type_generic),
            pygame.K_f: (self.op_distress, rcd.dist_type_carrying),
            pygame.K_r: (self.op_repair, None),
            pygame.K_t: (self.op_tractor_toggle, None),
            }

    def op_null(self, event, arg):
        pass

    def op_beam_down(self, event, arg):
        nt.send(cp_beam.data(2))

    def op_beam_up(self, event, arg):
        nt.send(cp_beam.data(1))

    def op_bomb(self, event, arg):
        nt.send(cp_bomb.data())

    def op_cloak_toggle(self, event, arg):
        if not me: return
        if me.flags & PFCLOAK:
            nt.send(cp_cloak.data(0))
        else:
            nt.send(cp_cloak.data(1))

    def op_det(self, event, arg):
        nt.send(cp_det_torps.data())

    def op_det_me(self, event, arg):
        if not me: return
        base = me.n * MAXTORP
        for x in range(base, base + MAXTORP):
            torp = galaxy.torp(x)
            if torp.status == TMOVE or torp.status == TSTRAIGHT:
                nt.send(cp_det_mytorp.data(x))

    def op_distress(self, event, arg):
        if not me: return
        mesg = rcd.pack(arg, cursor(), me, galaxy)
        if mesg: nt.send(cp_message.data(MDISTR | MTEAM, me.team, mesg))

    def op_docking_toggle(self, event, arg):
        if not me: return
        if me.flags & PFDOCKOK:
            nt.send(cp_dockperm.data(0))
        else:
            nt.send(cp_dockperm.data(1))

    def op_orbit(self, event, arg):
        nt.send(cp_orbit.data(1))

    def op_planet_lock(self, event, arg):
        nearest = galaxy.closest_planet(cursor())
        if nearest != me:
            nt.send(cp_planlock.data(nearest.n))

    def op_player_lock(self, event, arg):
        nearest = galaxy.closest_ship(cursor())
        if nearest != me:
            nt.send(cp_playlock.data(nearest.n))

    def op_practice(self, event, arg):
        nt.send(cp_practr.data())

    def op_pressor_toggle(self, event, arg):
        if not me: return
        nearest = galaxy.closest_ship(cursor())
        if nearest != me:
            if me.flags & PFPRESS:
                nt.send(cp_repress.data(0, nearest.n))
            else:
                nt.send(cp_repress.data(1, nearest.n))

    def op_repair(self, event, arg):
        nt.send(cp_repair.data(1))

    def op_shield_toggle(self, event, arg):
        if not me: return
        if me.flags & PFSHIELD:
            nt.send(cp_shield.data(0))
        else:
            nt.send(cp_shield.data(1))

    def op_tractor_toggle(self, event, arg):
        if not me: return
        nearest = galaxy.closest_ship(cursor())
        if nearest != me:
            if me.flags & PFTRACT:
                nt.send(cp_tractor.data(0, nearest.n))
            else:
                nt.send(cp_tractor.data(1, nearest.n))

    def op_warp(self, event, arg):
        nt.send(cp_speed.data(arg))

    def op_warp_half(self, event, arg):
        if me: self.op_warp(event, me.cap.s_maxspeed / 2)

    def op_warp_full(self, event, arg):
        if me: self.op_warp(event, me.cap.s_maxspeed)

    def op_warp_down(self, event, arg):
        if me: self.op_warp(event, me.speed - 1)

    def op_warp_up(self, event, arg):
        if me: self.op_warp(event, me.speed + 1)

class PhaseFlightGalactic(PhaseFlight):
    def __init__(self):
        PhaseFlight.__init__(self, 'galactic')
        
    def do(self):
        self.run = True
        screen.blit(background, (0, 0))
        g_planets.clear(screen, background)
        g_planets.update()
        pygame.display.update(g_planets.draw(screen))
        self.bg = screen.copy() # static planet background
        # FIXME: planets are not redrawn if changed
        self.cycle()
        
    def kb(self, event):
        global ph_flight
        if event.key == pygame.K_RETURN:
            ph_flight = ph_tactical
            self.run = False
        else:
            return PhaseFlight.kb(self, event)

    def update(self):
        b_reports.clear(screen, self.bg)
        b_warning.clear(screen, self.bg)
        g_players.clear(screen, self.bg)
        g_players.update()
        b_warning.update()
        b_reports.update()
        r_players = g_players.draw(screen)
        r_reports = b_reports.draw(screen)
        r_warning = b_warning.draw(screen)
        pygame.display.update(r_players+r_reports+r_warning)

class PhaseFlightTactical(PhaseFlight):
    def __init__(self):
        global background

        PhaseFlight.__init__(self, 'tactical')
        self.borders = Borders()

        self.co_g = (0, 15, 15) # cyan
        self.co_y = (15, 15, 0) # yellow
        self.co_r = (15, 0, 15) # purple

        self.bg_g = screen.copy()
        self.bg_g.fill(self.co_g)
        self.bg_y = screen.copy()
        self.bg_y.fill(self.co_y)
        self.bg_r = screen.copy()
        self.bg_r.fill(self.co_r)

        self.bg = self.bg_g
        self.co = self.co_g

    def do(self):
        global background

        self.saved_background = background
        self.run = True
        screen.blit(self.bg, (0, 0))
        self.cycle()
        background = self.saved_background
        
    def kb(self, event):
        global ph_flight
        if event.key == pygame.K_RETURN:
            ph_flight = ph_galactic
            self.run = False
        else:
            return PhaseFlight.kb(self, event)

    # FIXME: subgalactic in a corner, alpha blended
    # FIXME: console in a corner
    # FIXME: action menu items around edge
    # FIXME: menu item "?" or mouse-over, to do modal information
    # query on a screen object.

    def alert(self):
        """ if the alert status has changed, adjust the background colour """
        global background

        if me.flags & PFGREEN:
            bg = self.bg_g
        elif me.flags & PFYELLOW:
            bg = self.bg_y
        elif me.flags & PFRED:
            bg = self.bg_r
        if bg != background:
            background = bg
            self.bg = bg
            screen.blit(self.bg, (0, 0))
            pygame.display.flip()

    def update(self):
        """ clear, update, and redraw all tactical sprites and non-sprites """

        o_phasers = galaxy.phasers_undraw(self.co)
        o_borders = self.borders.undraw(self.co)
        b_reports.clear(screen, self.bg)
        b_warning.clear(screen, self.bg)
        t_torps.clear(screen, self.bg)
        t_players.clear(screen, self.bg)
        t_planets.clear(screen, self.bg)
        
        self.alert()
        t_planets.update()
        t_players.update()
        t_torps.update()
        b_warning.update()
        b_reports.update()
        
        r_planets = t_planets.draw(screen)
        r_players = t_players.draw(screen)
        r_weapons = t_torps.draw(screen)
        r_phasers = galaxy.phasers_draw()
        r_borders = self.borders.draw()
        r_reports = b_reports.draw(screen)
        r_warning = b_warning.draw(screen)
        
        pygame.display.update(o_phasers+o_borders+r_planets+r_players+r_weapons+r_phasers+r_borders+r_reports+r_warning)

        #r_debug = galaxy.torp_debug_draw()
        #pygame.display.update(r_debug)
        #r_debug = galaxy.ship_debug_draw()
        #pygame.display.update(r_debug)

class PhaseDisconnected(Phase):
    def __init__(self, screen):
        Phase.__init__(self)
        self.background("hubble-helix.jpg")
        x = screen.get_width()/2
        self.text('netrek', x, 100, 92)
        self.text(opt.chosen, x, 185, 64)
        self.text('disconnected', x, 255, 64)
        self.texts = Texts(self.diagnosis(), 50, 455, 12, 18)
        self.add_quit_button(self.quit)
        self.add_list_button(self.list)
        pygame.display.flip()
        self.run = True
        self.cycle()
        # FIXME: show last few lines of message log
        # FIXME: if freed by captain in clue game from player slot automatically return as an observer slot
        # FIXME: offer rejoin as player and rejoin as observer buttons

    def diagnosis(self):
        if sp_badversion.why == None:
            return ['Connection was closed by the server.',
                    '',
                    'You may have been idle for too long.',
                    'You may have a network problem.',
                    'You may have been ejected by vote.',
                    'You may have been freed by the captain in a clue game.',
                    'You may have been disconnected by the server owner.',
                    '',
                    'Technical data: read(2) returned zero on',
                    nt.diagnostics()]

        x = []
        s = ['Protocol version in CP_SOCKET is not supported by server.',
             'Access denied by server.',
             'No free slots on server queue.',
             'Banned from server.',
             'Game shutdown by server.',
             'Server daemon stalled, internal error.',
             'Server reports internal error.']

        # FIXME: how to contact a server owner, noted by Gerdesas, design as
        # either a new feature packet with sysdef text setting, or
        # default to first user@host in .motd if an old server.

        l = [['You have either connected to a server that does not support',
              'this client, or the server itself is insane.',
              '',
              'Try a different server,',
              'or report this to the server owner,',
              'or report this to the client developer.'],
             
             ['The server has your IP address, or a range of addresses, in a',
              'configuration file, due to a prior denial of service attack.',
              '',
              'Try a different server,',
              'or try a different service provider,',
              'or ask the server owner about it.'],
             
             ['The server was not able to place you in the queue, perhaps',
              'due to a denial of service attack happening right now.',
              '',
              'Or if you were in a clue game, the captain has freed your slot',
              'so that another player can join.',
              '',
              'Or in a pickup game the players ejected you.',
              '',
              'Try a different server,',
              'or rejoin as an observer of the clue game.'],
             
             ['The server has your IP address in the list of bans,',
              'usually because you were banned by the players or the owner.',
              '',
              'Try a different server,',
              'and if you were misbehaving try not to in future.'],
             
             ['The server was shutdown by the owner,',
              'probably only temporarily.',
              '',
              'Try a different server,',
              'or try this server later,',
              'or ask the server owner about it.']]

        try:
            x.append(s[sp_badversion.why])
        except:
            x.append('Unknown cause.')
        x.append('')
        try:
            for y in l[sp_badversion.why]:
                x.append(y)
        except:
            x.append('Try again later.')
        x.append('')
        x.append('Technical data: received SP_BADVERSION packet, reason code %d' % sp_badversion.why)
        return x

    def list(self, event):
        self.run = False

""" Main Program
"""

def mc_init():
    """ metaserver client socket initialisation """
    mc = MetaClient()
    # query metaserver early,
    # to make good use of pygame startup and splash delay
    mc.query(opt.metaserver)
    return mc

def nt_init():
    """ netrek client socket initialisation """
    nt = Client(sp)
    if opt.tcp_only:
        nt.mode_requested = COMM_TCP
    nt.cp_udp_req = cp_udp_req
    return nt

def pg_fd():
    """ lift the hood on pygame and find the file descriptor that it
    expects graphics events to arrive from, so that it can be used in
    select, contributed by coderanger on #pygame and #olpc-devel """
    try:
        w = pygame.display.get_wm_info()
        w = w['display']
        n = int(str(w)[23:-1], 16)
        n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
        n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
    except:
        print "unable to identify file descriptor of X socket, slowing"
        return

    if n > 255:
        print "the fd was too large, abondoning that line of reasoning, just guessing"
        n = 4
        
    nt.set_pg_fd(n)
    if mc: mc.set_pg_fd(n)

def pg_init():
    """ pygame initialisation """
    global t_planets, t_players, t_torps, g_planets, g_players, b_warning_sprite, b_warning, b_reports, background
    
    pygame.init()
    size = width, height = 1000, 1000
    # FIXME: #1187736408 support a full screen mode that's variable
    # depending on the environment
    if not opt.fullscreen :
        screen = pygame.display.set_mode(size)
    else:
        try:
            screen = pygame.display.set_mode(size, FULLSCREEN)
        except:
            screen = pygame.display.set_mode(size)

    # FIXME: #1187736407 support screen resolutions below 1000x1000

    # sprite groups
    t_planets = pygame.sprite.OrderedUpdates(())
    t_players = pygame.sprite.OrderedUpdates(())
    t_torps = pygame.sprite.OrderedUpdates(())
    g_planets = pygame.sprite.OrderedUpdates(())
    g_players = pygame.sprite.OrderedUpdates(())
    b_warning = pygame.sprite.OrderedUpdates()
    b_warning_sprite = WarningSprite()
    b_warning.add(b_warning_sprite)
    b_reports = pygame.sprite.OrderedUpdates()
    b_reports.add(ReportSprite())

    background = screen.copy()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # FIXME: allow user to select graphics theme, default on XO is to
    # be white with oysters, otherwise use stars, planets, and ships.
    pygame.display.flip()
    return screen

def pg_quit():
    """ pygame termination """
    pygame.quit()

def mc_choose_first():
    """ show splash screen, then server list, accept a choice, connect """
    ph_splash = PhaseSplash(screen)
    ph_servers = PhaseServers(screen, mc)

def mc_choose_again():
    """ requery metaserver, show server list, accept a choice, connect """
    mc.query(opt.metaserver)
    ph_servers = PhaseServers(screen, mc)

def nt_play_a_slot():
    """ keep playing on a server, until user chooses a quit option, or
    a list option to return to the server list """
    global ph_flight, ph_galactic, ph_tactical
    
    ph_outfit = PhaseOutfit(screen)
    ph_galactic = PhaseFlightGalactic()
    ph_tactical = PhaseFlightTactical()

    while True:
        # choose a team and ship
        ph_outfit.do()
        if ph_outfit.cancelled: break # quit or list chosen during outfit
        # at this point, team and ship choice is accepted by server
        while me.status == POUTFIT: nt.recv()
        ph_flight = ph_tactical
        while True:
            screen.blit(background, (0, 0))
            pygame.display.flip()
            ph_flight.do()
            if me.status == POUTFIT: break # ship has died

def nt_play():
    """ keep playing, until user chooses a quit option """
    if opt.server == None: mc_choose_first()
    while True:
        # at this point, a new connection to a server has just been established
        try:
            nt.send(cp_socket.data())
            nt.send(cp_feature.data('S', 0, 0, 1, 'FEATURE_PACKETS'))
            # PhaseQueue?
            # FIXME: if an SP_QUEUE packet is received, present this phase
            # FIXME: allow play on another server even while queued? [grin]
            if opt.name == '':
                ph_login = PhaseLogin(screen)
                if ph_login.cancelled:
                    if mc == None: break
                    # return to metaserver list
                    mc_choose_again()
                    continue

            nt_play_a_slot()

        except ServerDisconnectedError:
            PhaseDisconnected(screen)

        if mc == None: break

        # return to metaserver list
        mc_choose_again()

def main(args=[]):
    global opt, screen, mc, nt

    for line in WELCOME: print line
    print

    opt = netrek.opt.Parser(args).values
    mc = None
    if opt.server == None: mc = mc_init()
    nt = nt_init()
    if opt.server != None:
        opt.chosen = opt.server
        if not nt.connect(opt.chosen, opt.port):
            print "connection failed"
            # server was requested on command line, but not available
            return 1
    screen = pg_init()
    pg_fd()

    nt_play()
    ic.statistics()
    pg_quit()
    return 0

# FIXME: very little reason for outfit phase, default to automatically re-enter
# FIXME: planets to be partial alpha in tactical view as ships close in?

# socket http://docs.python.org/lib/socket-objects.html
# select http://docs.python.org/lib/module-select.html
# struct http://docs.python.org/lib/module-struct.html
# built-ins http://docs.python.org/lib/built-in-funcs.html

# FIXME: add fast quit, which answers SP_PICKOK with -1 and then CP_QUIT

# FIXME: add graphic indicator of connection status
# FIXME: discover servers from a cache

# FIXME: when other slot frees, free all torps

# FIXME: add a help aka documentation button on metaserver list, also
# accessible from other modes but will force a disconnection from
# server, to contain tutorial, ship classes, and rank information.

# FIXME: mouse-over hint for word "clue", explain terms (says Petria)

# FIXME: list buttons do not show server list if --server used, avoid
# rendering them.

# FIXME: 'k' key, 'p' key
