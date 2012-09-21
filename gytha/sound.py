import os
import pygame

def prepare(opt_sounds):

    global sounds
    sounds = {}

    def load(key, name):
        try:
            sounds[key] = pygame.mixer.Sound(os.path.join(opt_sounds, name))
        except:
            print 'sound not found, key', key, 'name', name

    load('tada1', '60443__jobro__tada1.wav')
    load('tada2', '60444__jobro__tada2.wav')
    load('tada3', '60445__jobro__tada3.wav')

def play(key):
    if key in sounds:
        sounds[key].play()

