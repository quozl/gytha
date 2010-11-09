""" cache of pygame objects, to avoid repeated file I/O to images that
are used frequently in different ways, as an "strace -e open" shows
that a second pygame.image.load for the same file causes the file to
be opened again. """
import pygame, os, time

class IC:
    """ an image cache """
    def __init__(self):
        self.cache = {}
        self.cache_rotated = {}
        self.cache_scale2xed = {}
        self.hits = self.miss = 0
        self.hits_rotated = self.miss_rotated = 0
        self.paths = ['/usr/share/gytha/images/', 'images/']

    def read(self, name):
        """ try package location, otherwise try local directory """
        image = None
        for path in self.paths:
            try:
                image = pygame.image.load(path + name)
            except pygame.error:
                pass
        if not image:
            raise pygame.error, "no such file %s" % name
        return pygame.Surface.convert_alpha(image)

    def get(self, name):
        """ get an image from cache, normal """
        if name not in self.cache:
            self.cache[name] = self.read(name)
            self.miss += 1
        else:
            self.hits += 1
        return self.cache[name]

    def get_rotated(self, name, angle):
        """ get an image from cache, rotated """
        if (name, angle) not in self.cache_rotated:
            unrotated = self.get(name)
            self.miss_rotated += 1
            rotated = pygame.transform.rotate(unrotated, -angle)
            self.cache_rotated[(name, angle)] = rotated
        else:
            self.hits_rotated += 1
        return self.cache_rotated[(name, angle)]

    def get_scale2xed(self, name):
        """ get an image from cache, scaled up """
        if (name) not in self.cache_scale2xed:
            unscaled = self.get(name)
            try:
                scaled = pygame.transform.smoothscale(unscaled, (2000, 2000))
            except:
                scaled = pygame.transform.scale2x(unscaled)
            self.cache_scale2xed[(name)] = scaled
        return self.cache_scale2xed[(name)]

    def preload_scan(self):
        self.names = []
        for path in self.paths:
            for dirpath, dirnames, filenames in os.walk('images'):
                for name in filenames:
                    if '.png' not in name and '.jpg' not in name:
                        continue
                    if name not in self.names:
                        self.names.append(name)
        import random
        self.names.sort()

    def preload_early(self):
        """ preload cache with known large images that cost more than
        a hundredth of a second on the developer's hardware ... these
        images will certainly cause the splash bouncer update to
        stumble """
        self.get('team-box-fed.png')
        self.get('team-box-kli.png')
        self.get('team-box-ori.png')
        self.get('team-box-rom.png')
        self.get('hubble-crab.jpg')
        self.get('hubble-helix.jpg')
        self.get('hubble-orion.jpg')
        self.get('hubble-spire.jpg')
        self.get('exp-04.png')
        self.get('exp-05.png')
        self.get('exp-06.png')

    def preload_one(self):
        """ preload just one image, intended to be called on updates
        of the splash bouncer """
        for name in self.names:
            t0 = time.time()
            self.get(name)
            self.names.remove(name)
            t1 = time.time()
            el = t1 - t0
            if el > 0.01:
                print "image was slow to load, %.3f sec file %s" % (el, name)
            return

    def preload_rest(self):
        """ preload the remaining images in the scan """
        for name in self.names:
            self.get(name)
            self.names.remove(name)

    def statistics(self):
        """ calculate and print cache statistics """
        if self.miss > 0:
            rate = self.hits * 100 / (self.hits + self.miss)
        else:
            rate = 0
        if self.miss_rotated > 0:
            rate_rotated = self.hits_rotated * 100 / \
                (self.hits_rotated + self.miss_rotated)
        else:
            rate_rotated = 0
        print "IC: normal hits=%d miss=%d rate=%d%% n=%d" % \
              (self.hits, self.miss, rate, len(self.cache))
        print "IC: rotate hits=%d miss=%d rate=%d%% n=%d" % \
              (self.hits_rotated, self.miss_rotated, rate_rotated, \
               len(self.cache_rotated))
        names = []
        for key in self.cache:
            if key not in names:
                names.append(key)
        for key in self.cache_rotated:
            (name, angle) = key
            if name not in names:
                names.append(name)
        for key in self.cache_scale2xed:
            (name) = key
            if name not in names:
                names.append(name)
        names.sort()
        unused = []
        for name in names:
            print "used image", name
        for dirpath, dirnames, filenames in os.walk('images'):
            for name in filenames:
                if '.png' not in name and '.jpg' not in name:
                    continue
                if name not in names:
                    unused.append(name)
        unused.sort()
        for name in unused:
            print "unused image", name

class FC:
    """ a font cache """
    def __init__(self):
        self.cache = {}

    def read(self, name, size):
        """ try system font location, otherwise use default font """
        if name == None:
            return pygame.font.Font(None, size)
        path = '/usr/share/fonts/truetype/ttf-dejavu/'
        try:
            return pygame.font.Font(path + name, size)
        except IOError:
            return pygame.font.Font(None, size)

    def get(self, name, size):
        """ get a font from cache """
        key = (name, size)
        if key not in self.cache:
            self.cache[key] = self.read(name, size)
        return self.cache[key]

ic = IC()
fc = FC()
