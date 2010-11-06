import pygame
from cache import ic, fc

class MultipleImageSprite(pygame.sprite.Sprite):
    """ a sprite class consisting of multiple images overlaid
        the images are blitted over each other in the order they are added
        all images share a common centre
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


class SpriteBacked(pygame.sprite.Sprite):
    """ a sprite on the existing background """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()

    def clear(self):
        return self.screen.blit(self.background, self.rect)

    def suck(self):
        self.background = self.screen.subsurface(self.rect.clip(self.screen.get_rect())).copy()

    def blit(self):
        return self.screen.blit(self.image, self.rect)

    def draw(self):
        self.suck()
        return self.blit()

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Clickable:
    """ a clickable screen object, the clicked callback is called when
    a mouse up event occurs within the object, after a mouse down event
    had been previously seen. """
    def __init__(self, clicked, buttons=[1]):
        self.clicked = clicked
        self.arm = False
        self.buttons = [1]

    def md(self, event):
        if not self.rect.collidepoint(event.pos[0], event.pos[1]):
            self.arm = False
            return False
        if event.button not in self.buttons:
            self.arm = False
            return True
        self.arm = True
        return True

    def mu(self, event):
        if not self.rect.collidepoint(event.pos[0], event.pos[1]):
            self.arm = False
            return False
        if event.button not in self.buttons:
            self.arm = False
            return True
        if not self.arm: return True
        self.clicked(event)
        self.arm = False
        return True


class ClickableHot(Clickable):
    """ a clickable screen object, with a hot area highlight, so that
    when the mouse moves into the area the highlight is drawn, and
    cleared when the mouse leaves.  Descendent is responsible for
    setting up image_hot and image_cold. """
    def __init__(self, clicked):
        Clickable.__init__(self, clicked)
        self.hot = False

    def mm(self, event):
        if not self.rect.collidepoint(event.pos[0], event.pos[1]):
            if self.hot:
                self.hot = False
                return True
        else:
            if not self.hot:
                self.hot = True
                return True
        return False

    def update(self):
        if self.hot:
            if self.image != self.image_hot:
                self.image = self.image_hot
                return True
        else:
            if self.image != self.image_cold:
                self.image = self.image_cold
                return True
        return False

    def check_cursor_under(self):
        """ make button hot if cursor was left in the area """
        (mx, my) = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            self.hot = True
            self.update()


class Icon(SpriteBacked):
    """ a sprite for icons, a simple image """
    def __init__(self, name, x, y, rf=None, rfa=None):
        self.image = ic.get(name)
        if rf:
            self.rect = rf(self.image.get_rect, rfa)
        else:
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
    def __init__(self, text, rf, rfa, size=18, colour=(255, 255, 255)):
        font = fc.get('DejaVuSans.ttf', size)
        self.image = font.render(text, 1, colour)
        if rf: self.rect = rf(self.image.get_rect, rfa)
        SpriteBacked.__init__(self)


class TextsLine(SpriteBacked):
    def __init__(self, text, x, y, size=18):
        font = fc.get('DejaVuSansMono.ttf', size)
        self.image = font.render(text, 1, (255, 255, 255))
        self.rect = self.image.get_rect(left=x, top=y)
        SpriteBacked.__init__(self)


class Texts:
    """
    a group of sprites for lines of text, one sprite per line
    """
    def __init__(self, texts, x, y, lines=24, size=18):
        self.screen = pygame.display.get_surface()
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
        self.rects = self.group.draw(self.screen)
        return self.rects

    def add(self, text):
        if self.lines < 1: return None
        sprite = self._new(text)
        sprite.draw()
        return sprite


class TextButton(Text, Clickable):
    def __init__(self, clicked, text, rf, rfa, size, colour):
        self.text = text
        Text.__init__(self, text, rf, rfa, size, colour)
        Clickable.__init__(self, clicked)


class IconButton(Icon, Clickable):
    def __init__(self, clicked, image, rf, rfa):
        Icon.__init__(self, image, 0, 0, rf, rfa)
        Clickable.__init__(self, clicked)


class IconTextButton(ClickableHot, Text, Icon):
    def __init__(self, clicked, swap, image, text, size, colour, rf, rfa):
        # create the icon part and keep
        Icon.__init__(self, image, 0, 0, None, None)
        gs = self.image
        gr = gs.get_rect()
        # create the text part and keep
        Text.__init__(self, text, None, None, size, colour)
        ts = self.image
        tr = ts.get_rect()
        # define size to hold both
        pad = 4
        w = pad + gr.width + pad + tr.width + pad
        h = max(gr.height, tr.height)
        # make image to hold both
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        # lateral swap icon and text if requested
        if swap:
            (gs, gr, ts, tr) = (ts, tr, gs, gr)
        # blit both into image
        gr.left = pad
        gr.centery = h/2
        self.image.blit(gs, gr)
        tr.left = gr.right + 1 + pad
        tr.centery = gr.centery
        self.image.blit(ts, tr)
        # align image per rf/rfa
        self.rect = rf(self.image.get_rect, rfa)
        self.image_cold = self.image
        # prepare a highlight image
        self.image_hot = self.image.copy()
        pygame.draw.rect(self.image_hot, (128, 128, 255),
                         self.image_hot.get_rect(), 1)
        ClickableHot.__init__(self, clicked)


class HorizontalAssemblyButton(ClickableHot, SpriteBacked):
    """ a button composed of multiple image surfaces set side by side,
    where each item passed also includes an x coordinate
    preference. """
    def __init__(self, clicked, items, pad, rf, rfa):
        ClickableHot.__init__(self, clicked)
        SpriteBacked.__init__(self)
        # determine the surface dimensions
        x = y = 0
        for item in items:
            (surface, position) = item
            if position:
                x = max(x, position)
            x += surface.get_width() + pad
            y = max(y, surface.get_height())
        # create an image to hold the surfaces
        self.image = pygame.Surface((x, y), pygame.SRCALPHA, 32)
        # place each surface into the image, left to right
        x = 0
        for item in items:
            (surface, position) = item
            if position:
                x = position
            rect = surface.get_rect(left=x, centery=y/2)
            self.image.blit(surface, rect)
            x += rect.width + pad
        self.rect = rf(self.image.get_rect, rfa)
        self.image_cold = self.image
        # prepare a highlight image
        self.image_hot = self.image.copy()
        pygame.draw.rect(self.image_hot, (128, 128, 255),
                         self.image_hot.get_rect(), 1)


class Field:
    def __init__(self, prompt, value, x, y, echo=True):
        self.screen = pygame.display.get_surface()
        self.value = value
        self.echo = echo
        self.fn = fn = fc.get('DejaVuSans.ttf', 36)
        self.sw = sw = self.screen.get_width()
        self.sh = sh = self.screen.get_height()
        # place prompt on screen
        self.ps = ps = fn.render(prompt, 1, (255, 255, 255))
        self.pc = pc = (x, y)
        self.pr = pr = ps.get_rect(topright=pc)
        self.pg = self.screen.subsurface(self.pr).copy()
        r1 = self.screen.blit(ps, pr)
        # highlight entry area
        self.br = pygame.Rect(pr.right, pr.top, sw - pr.right - 200, pr.height)
        self.bg = self.screen.subsurface(self.br).copy()
        pygame.display.update(r1)
        self.enter()

    def highlight(self):
        self.screen.blit(self.bg, self.br)
        return pygame.draw.rect(self.screen, (128, 128, 255), self.br, 1)

    def unhighlight(self):
        return self.screen.blit(self.bg, self.br)

    def draw(self):
        value = self.value
        if not self.echo: value = '*' * len(self.value)
        ts = self.fn.render(value, 1, (255, 255, 255))
        tr = ts.get_rect(topleft=self.pc)
        tr.left = self.pr.right
        return self.screen.blit(ts, tr)

    def undraw(self):
        return self.screen.blit(self.pg, self.pr)

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
        r1 = self.highlight()
        r2 = self.draw()
        pygame.display.update([r1, r2])

    def backspace(self):
        self.value = self.value[:-1]
        self.redraw()

    def delete(self):
        self.value = ""
        self.redraw()

