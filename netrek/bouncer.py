import pygame, math
from sprites import Icon


class Bouncer:
    """ two torps following an orbital ellipse around an invisible mass """
    def __init__(self, ex, ey, cx, cy, n1='torp-me.png', n2='torp-me.png'):
        self.ex = ex
        self.ey = ey
        self.cx = cx
        self.cy = cy
        self.l = Icon(n1, self.cx+50, self.cy)
        self.r = Icon(n2, self.cx-50, self.cy)
        self.position(0, 1)
        self.l.draw()
        self.r.draw()

    def position(self, fuse, fuse_max):
        x = self.ex * math.sin(fuse * math.pi / fuse_max)
        y = self.ey * math.cos(fuse * math.pi / fuse_max)
        self.l.move(self.cx - x, self.cy - y)
        self.r.move(self.cx + x, self.cy + y)

    def update(self, fuse, fuse_max):
        r = []
        r.append(self.l.clear())
        r.append(self.r.clear())
        self.position(fuse, fuse_max)
        r.append(self.l.draw())
        r.append(self.r.draw())
        pygame.display.update(r)
