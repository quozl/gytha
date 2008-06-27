import pygame

class IC:
    """ an image cache
    """
    def __init__(self):
        self.cache = {}
        self.cache_rotated = {}
        self.hits = self.miss = 0
        self.hits_rotated = self.miss_rotated = 0

    def read(self, name):
        try:
            path = '/usr/share/netrek-client-pygame/images/' 
            image = pygame.image.load(path + name)
        except:
            image = pygame.image.load('images/' + name)
        return pygame.Surface.convert_alpha(image)

    def get(self, name):
        if name not in self.cache:
            self.cache[name] = self.read(name)
            self.miss += 1
        else:
            self.hits += 1
        return self.cache[name]

    def get_rotated(self, name, angle):
        if (name, angle) not in self.cache_rotated:
            unrotated = self.get(name)
            self.miss_rotated += 1
            rotated = pygame.transform.rotate(unrotated, -angle)
            self.cache_rotated[(name, angle)] = rotated
        else:
            self.hits_rotated += 1
        return self.cache_rotated[(name, angle)]

    def statistics(self):
        if self.miss > 0:
            self.rate = self.hits * 100 / (self.hits + self.miss)
        else:
            self.rate = 0
        if self.miss_rotated > 0:
            self.rate_rotated = self.hits_rotated * 100 / (self.hits_rotated + self.miss_rotated)
        else:
            self.rate_rotated = 0
        print "IC: normal hits=%d miss=%d rate=%d%% n=%d" % (self.hits, self.miss, self.rate, len(self.cache))
        print "IC: rotate hits=%d miss=%d rate=%d%% n=%d" % (self.hits_rotated, self.miss_rotated, self.rate_rotated, len(self.cache_rotated))

class FC:
    """ a font cache
    """
    def __init__(self):
        self.cache = {}

    def read(self, name, size):
        if name == None:
            return pygame.font.Font(None, size)
        path = '/usr/share/fonts/truetype/ttf-dejavu/'
        try:
            return pygame.font.Font(path + name, size)
        except:
            return pygame.font.Font(None, size)

    def get(self, name, size):
        key = (name, size)
        if key not in self.cache:
            self.cache[key] = self.read(name, size)
        return self.cache[key]
