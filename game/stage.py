import os, pygame, time
import random
from pygame.locals import *
from sprites import *
from bubblegrid import *
import utils

class Stage():
    def __init__(self, screen):
        self.screen = screen
        self.initialise()
        self.debug = False

    def initialise(self):
        #Initialize Everything
        pygame.display.flip()

        self.game_paused = False
        #sounds
        self.sounds = {};
        self.sounds['plop'] = utils.load_sound('plop.wav')

        #Create The Backgound
        self.background, foo = utils.load_image('background.png')

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        #group that stores all bubbles
        self.bubbles            = pygame.sprite.Group()
        self.flying_scores      = pygame.sprite.Group()

        #game variables
        self.score  = Score_Meter((10,10,10,10))
        self.flying_scores.add(self.score)


        self.bubble_grid = Bubblegrid(10,15,self.bubbles)

        #group for information sprites in the screen, should be rendered the last one

        self.font = utils.load_font('chitown.ttf', 20)

        self.game_started   = False
        self.game_finished  = False
        self.level_finished = False


    def handle_event(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE and self.game_finished == False:
                self.game_finished = True
            elif event.type == KEYDOWN and self.game_started == False:
                self.game_started = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                exploded = self.bubble_grid.process_click(pos)
                for exploded_bubble in exploded:
                    self.score.add_score(100)
                    a = self.sounds['plop']
                    a.play()
                    flying_score = Flying_Score(exploded_bubble, 100)
                    self.flying_scores.add(flying_score)

        return False

    #Main Loop, return  bool = if the game is over
    def loop(self):
        exit = self.handle_event()
        self.screen.blit(self.background, (0, 0))
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
        self.bubbles.update()
        self.flying_scores.update()

        if self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 230))
        else:
            self.bubbles.draw(self.screen)
            self.flying_scores.draw(self.screen)

        #draw all the groups of sprites
        pygame.display.flip()
        return False

    #Game Over




