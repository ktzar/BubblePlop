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

        self.bubble_size    = (16,18)
        self.bubble_offsets = (50,100)
        self.grid_size      = (20,30)

        #Create The Backgound
        self.background, foo = utils.load_image('background.png')

        #game variables
        self.score  = 0

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        #group that stores all bubbles
        self.bubbles    = pygame.sprite.Group()


        #group for information sprites in the screen, should be rendered the last one

        self.font = utils.load_font('saloon.ttf', 20)

        self.game_started   = False
        self.game_finished  = False
        self.level_finished = False

        self.bubbles_grid = []
        for i in range(self.grid_size[0]):
            row = []
            for j in range(self.grid_size[1]):
                bubble = Bubble(pygame.Rect(\
                        self.bubble_offsets[0]+i*self.bubble_size[0],\
                        self.bubble_offsets[1]+j*(self.bubble_size[1])+(i%2)*self.bubble_size[1]/2,\
                        self.bubble_size[0],self.bubble_size[1]))
                row.append(bubble)
                self.bubbles.add(bubble)
            self.bubbles_grid.append(row)


    def find_surrounding(self,x,y,rec=0):
        if rec > 6:
            return []
        matched = [[x,y]]
        if self.bubbles_grid[x][y-1].value == self.bubbles_grid[x][y].value:
            returned = self.find_surrounding(x,y-1, rec+1)
            for ret in returned:
                matched.append(ret)
        if self.bubbles_grid[x][y+1].value == self.bubbles_grid[x][y].value:
            returned = self.find_surrounding(x,y+1, rec+1)
            for ret in returned:
                matched.append(ret)
        if self.bubbles_grid[x+1][y].value == self.bubbles_grid[x][y].value:
            returned = self.find_surrounding(x+1,y, rec+1)
            for ret in returned:
                matched.append(ret)
        if self.bubbles_grid[x-1][y].value == self.bubbles_grid[x][y].value:
            returned = self.find_surrounding(x-1,y, rec+1)
            for ret in returned:
                matched.append(ret)
        if x%2 == 0:
            if self.bubbles_grid[x-1][y-1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x-1,y-1, rec+1)
                for ret in returned:
                    matched.append(ret)
            if self.bubbles_grid[x+1][y-1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x+1,y-1, rec+1)
                for ret in returned:
                    matched.append(ret)
        else:
            if self.bubbles_grid[x-1][y+1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x-1,y+1, rec+1)
                for ret in returned:
                    matched.append(ret)
            if self.bubbles_grid[x+1][y+1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x+1,y+1, rec+1)
                for ret in returned:
                    matched.append(ret)
        print "matched"
        print matched
        return matched


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
                pos_x = (pos[0]-self.bubble_offsets[0]) / self.bubble_size[0]

                #clicks in even columns need to be shifted half a bubble's size
                offset_y = ((pos_x)%2) *(self.bubble_size[1]/2)
                print offset_y

                pos_y = (pos[1]-self.bubble_offsets[1]-offset_y) / self.bubble_size[1]

                if  pos_x < 0 or pos_x > self.grid_size[0] or \
                        pos_y < 1 or pos_y > self.grid_size[1]:
                    print "Aim better mate"
                else:
                    print "{0}:{1}".format(pos_x,pos_y)
                    surrounding_bubbles = self.find_surrounding(pos_x,pos_y)
                    for surrounding_bubble in surrounding_bubbles:
                        self.bubbles_grid[surrounding_bubble[0]][surrounding_bubble[1]].kill()#.rect.left = 0
                    self.bubbles_grid[pos_x][pos_y].kill()#.rect.left = 0

        return False

    #Main Loop, return  bool = if the game is over
    def loop(self):
        exit = self.handle_event()
        pygame.display.flip()
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


        #Draw background and HUD
        score_text = "Score: {0}".format(self.score)
        text = self.font.render(score_text, 1, (255, 255, 255))
        text_shadow = self.font.render(score_text, 1, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text_shadow, (12, 12))
        self.screen.blit(text, (10, 10))

        #draw the level
        self.bubbles.update()

        if self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 230))
        else:
            self.bubbles.draw(self.screen)

        #draw all the groups of sprites
        pygame.display.flip()
        return False

    #Game Over




