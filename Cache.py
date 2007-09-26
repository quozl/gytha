import pygame

class IC:
    """ an image cache
    """
    def __init__(self):
        self.cache = {}
        self.cache_rotated = {}

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
        return self.cache[name]

    def get_rotated(self, name, angle):
        if (name, angle) not in self.cache_rotated:
            unrotated = self.get(name)
            rotated = pygame.transform.rotate(unrotated, -angle)
            self.cache_rotated[(name, angle)] = rotated
        return self.cache_rotated[(name, angle)]
        
class FC:
    """ a font cache
    """
    def __init__(self):
        self.cache = {}

    def read(self, name, size):
        font = pygame.font.Font(name, size)
        return font

    def get(self, name, size):
        key = (name, size)
        if key not in self.cache:
            self.cache[key] = self.read(name, size)
        return self.cache[key]
