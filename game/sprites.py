import os, pygame, time, random
from pygame.locals import *
import utils

#A bubble with random value=colour
#can be moved to the position in the bottom with animation
class Bubble(pygame.sprite.Sprite):
    #TODO add the size of the bubble here
    #Images to choose from
    images = ['bubble_1.png', 'bubble_2.png']#, 'bubble_3.png', 'bubble_4.png']#, 'bubble_5.png']

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.value      = random.randint(1,len(Bubble.images))
        self.image, self.rect = utils.load_image(Bubble.images[self.value-1])
        self.rect.top   = position.top
        self.target_top = position.top
        self.rect.left  = position.left

    #Only change the target to trigger animation
    def move_down(self):
        self.target_top = self.target_top + 32

    #Animate the bubble if the target position is different than the current one
    def update(self):
        if self.rect.top < self.target_top:
            self.rect.top += ((self.target_top - self.rect.top)/5) + 2
            if self.rect.top > self.target_top:
                self.rect.top = self.target_top

#Sprite that shows a number fading out, when faded dies
class Flying_Score(pygame.sprite.Sprite):

    def __init__(self, position, score):
        self.age = 0 #To animate it and decide when to kill()
        pygame.sprite.Sprite.__init__(self)
        font        = utils.load_font('chitown.ttf', 20)
        score       = '{0}'.format(score)
        surf_text   = font.render(score, 2, (255,255,255))
        self.rect   = position
        self.image  = pygame.Surface(font.size(score))
        #Blitting into a new Surface is needed to apply alpha, doesn't work in the surface from font.render
        self.image.blit(surf_text, (0,0))
        self.image.set_colorkey((0,0,0))

    #Move upwards and dither a bit
    def update(self):
        new_alpha = max(0,255-self.age * 10)
        self.image.set_alpha (new_alpha)
        self.age += 1
        self.rect.top -= self.age/4 + random.randint(1,2)
        if self.age > 25:
            self.kill()

class Score_Meter(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.target_score = 0
        self.rect = position
        self.font = utils.load_font('chitown.ttf', 36)
        self.reload_image()

    def reload_image(self):
        score_text = 'Score: {0}'.format((self.score))
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))
        self.image = pygame.Surface(self.font.size(score_text))
        self.image.blit(text_shadow, (0,0))
        self.image.blit(text, (0,0))
        self.image.set_colorkey((0,0,0))

    def add_score(self, score):
        self.target_score += score

    def update(self):
        if self.target_score > self.score:
            self.score += (self.target_score - self.score ) / 10 + random.randint(5,9)
            if self.score > self.target_score:
                self.score = self.target_score
            self.reload_image()

