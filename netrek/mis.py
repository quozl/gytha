import pygame

class MultipleImageSprite(pygame.sprite.Sprite):
    """ a sprite class consisting of multiple images overlaid
        the images are blitted over each other in the order they are added
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def mi_begin(self):
        self.ml = []
        self.mr = None

    def mi_add(self, image, rect):
        self.ml.append((image, rect))
        if self.mr == None:
            self.mr = rect
        else:
            self.mr = pygame.Rect.union(self.mr, rect)
            
    def mi_add_image(self, image):
        rect = image.get_rect()
        self.mi_add(image, rect)

    def mi_commit(self):
        width = self.mr.width
        height = self.mr.height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        for x in self.ml:
            (image, rect) = x
            rect.center = (width/2, height/2)
            self.image.blit(image, rect)
        self.rect = pygame.Rect(self.image.get_rect())
    
