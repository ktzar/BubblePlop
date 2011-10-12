import os, pygame, time, random
from pygame.locals import *
import utils

class Bubble(pygame.sprite.Sprite):
    #TODO add the size of the bubble here
    images = ['bubble_1.png', 'bubble_2.png', 'bubble_3.png', 'bubble_4.png']#, 'bubble_5.png']

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = random.randint(1,len(Bubble.images))
        self.image, self.rect = utils.load_image(Bubble.images[self.value-1])
        self.rect.top = position.top
        self.target_top = position.top
        self.rect.left = position.left

    def move_down(self):
        self.target_top = self.target_top + 32


    def update(self):
        if self.rect.top < self.target_top:
            self.rect.top += ((self.target_top - self.rect.top)/5) + 2
            if self.rect.top > self.target_top:
                self.rect.top = self.target_top
        pass

class Flying_Score(pygame.sprite.Sprite):

    def __init__(self, position, score):
        self.age = 0
        pygame.sprite.Sprite.__init__(self)
        font = utils.load_font('chitown.ttf', 20)
        score = '{0}'.format(score)
        surf_text = font.render(score, 2, (255,255,255))
        self.image = pygame.Surface(font.size(score))
        self.image.blit(surf_text, (0,0))
        self.rect = position
        self.image.set_colorkey((0,0,0))

    def update(self):
        new_alpha = max(0,255-self.age * 25)
        self.image.set_alpha (new_alpha)
        self.age += 1
        self.rect.top -= self.age/2 + random.randint(1,10)
        if self.age > 11:
            self.kill()
