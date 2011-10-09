import os, pygame, time, random
from pygame.locals import *
import utils

class Bubble(pygame.sprite.Sprite):

    images = ['bubble_1.png', 'bubble_2.png', 'bubble_3.png', 'bubble_4.png', 'bubble_5.png']

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(Bubble.images[random.randint(0,len(Bubble.images)-1)])
        self.rect.top = position.top
        self.rect.left = position.left

    def update(self):
        pass


