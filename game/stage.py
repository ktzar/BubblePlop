import os, pygame, time
import random
from pygame.locals import *
from sprites import *
import utils

class Stage():
    def __init__(self, screen):
        self.screen = screen
        self.initialise()

    def initialise(self):
        #Initialize Everything
        pygame.display.flip()

        self.game_paused = False
        #sounds
        self.sounds = {};
        self.sounds['plop'] = utils.load_sound('plop.wav')

        #Create The Backgound
        self.background, foo = utils.load_image('background.png')

        #game variables
        self.score  = 0

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        #group that stores all bubbles
        self.bubbles    = pygame.sprite.Group()

        self.bubbles.add(Bubble(pygame.Rect((200,100, 10, 10))))

        #group for information sprites in the screen, should be rendered the last one

        self.font = utils.load_font('saloon.ttf', 20)

        self.game_started   = False
        self.game_finished  = False
        self.level_finished = False


    def handle_keys(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == False:
                self.game_finished = True
            elif event.type == KEYDOWN and self.game_started == False:
                self.game_started = True
        return False

    #Main Loop, return  bool = if the game is over
    def loop(self):
        exit = self.handle_keys()
        print self.game_finished
        if self.game_finished:
            return True
        if exit == True:
            return True

        if self.game_started == False:
            start_text = self.font.render('Press any key to start', 2, (255,255,255))
            self.screen.blit(start_text, (100, 200))
            pygame.display.flip()
            return False

        if self.game_paused == 1:
            start_text = self.font.render('Game paused', 2, (255,255,255))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return False

        #draw the level
        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.bubbles.sprites())
        all_sprites.update()

        #self.screen.blit(all_sprites, (0, 0))
        all_sprites.draw(self.screen)

        #Move and draw the background
        score_text = "Score: {0}".format(self.score)
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text_shadow, (12, 12))
        self.screen.blit(text, (10, 10))

        if self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 230))
        else:
            all_sprites.draw(self.screen)

        #draw all the groups of sprites
        pygame.display.flip()
        return False

    #Game Over




