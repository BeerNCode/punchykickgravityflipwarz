from PIL import Image
import pygame
import colours

imageFile = "world.png"

class World:
    
    def __init__(self):
        self.tiles = []
        #self.index

    def get_world(self, screen):
        img = Image.open(imageFile)
        rgb_im = img.convert('RGB')

        width = rgb_im.size[1]

        for i in range (0,rgb_im.size[0]-1):
            for j in range (0,rgb_im.size[1]-1):
                if (rgb_im.getpixel((i,j)) == (0,0,0)):
                    #index = self.get_index(i, j, width)
                    #self.tiles[index] = 1
                    pygame.draw.rect(screen, colours.BLACK, [i*1, j*1, 1, 1], 0)
                else:
                    #self.tiles[index] = 0
                    pygame.draw.rect(screen, colours.WHITE, [i*1, j*1, 1, 1], 0)

    def get_index(self, x, y, width):
        return y * width + x    
