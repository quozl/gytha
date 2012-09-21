import os
import random
import pygame

def prepare(opt_sounds):

    global sounds
    sounds = {}

    def load(key, name):
        try:
            sounds[key] = pygame.mixer.Sound(os.path.join(opt_sounds, name))
        except:
            print 'sound not found, key', key, 'name', name

    load('tada1', '60443__jobro__tada1.ogg')
    load('tada2', '60444__jobro__tada2.ogg')
    load('tada3', '60445__jobro__tada3.ogg')
    load('click', 'click.ogg')
    load('death', '46492__phreaksaccount__shields1.ogg')
    load('gain', '57204__jace__men-shouting-hey.ogg')
    load('loss', '79671__joedeshon__slide-whistle-down-01.ogg')
    load('dramatic', '76058__digifishmusic__dramatic2.ogg')
    load('conquer', '31169__lonemonk__approx-850-enthusiast-audience.ogg')
    load('phaser', '27568__suonho__memorymoon-space-blaster-plays.ogg')
    load('inbound', '27568__suonho__memorymoon-space-blaster-plays-reverse.ogg')

def play(key):
    if key in sounds:
        sounds[key].play()

def play_if(key):
    if key in sounds:
        # this check proves to be unreliable, false positive if sound
        # recently played
        if sounds[key].get_num_channels():
            return
        sounds[key].play()

def texplode(distance):
    if distance < 300:
        play('click') # taps on hull

def conquer():
    # sample needs to be longer than the parade so that it does not repeat
    play_if('conquer')

n = 0
def achievement():
    global n

    a = ['tada1', 'tada2', 'tada3']
    play_if(a[n])
    n += 1
    if n > 2:
        n = 0
