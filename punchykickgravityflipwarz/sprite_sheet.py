import pygame

class SpriteSheet(object):
    def __init__(self, filename, colour_key=(255, 255, 255)):
        self.sheet = None
        self.filename = filename
        self.colour_key = colour_key    
        
    def image_at(self, rectangle):
        if self.sheet is None:
            self.sheet = pygame.image.load(self.filename).convert()

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.colour_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects):
        return [self.image_at(rect) for rect in rects]
    
    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups)
