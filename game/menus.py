'''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''
import pygame
from pygame.locals import *
import utils
import math
import pickle
import highscore
from highscore import *

class Abstract_Menu():
    def __init__(self, screen):
        self.font = utils.load_font('chitown.ttf', 24)
        self.background, foo    = utils.load_image('background.png')
        self.logo, foo          = utils.load_image('logo.png')
        self.screen = screen
        self.chosen_option = 0
        self.age = 0
        self.selected_option = -1
        self.events = [] #So the subclasses can inspect input events
        self.finished = False
        self.line_height = 60
        self.left_margin = 152

    def handle_keys(self):
        #Handle Input Events
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:                 
                if event.key == K_UP:
                    self.option_up()
                elif event.key == K_DOWN:
                    self.option_down()
                elif event.key == K_RETURN or event.key == K_LEFT or event.key == K_RIGHT:
                    self.selected_option = self.chosen_option
        return True

    #Select next option
    def option_down(self):
        if self.chosen_option != len(self.options)-1:
            self.chosen_option += 1

    #Select previous option
    def option_up(self):
        if self.chosen_option != 0:
            self.chosen_option -= 1

    #show background, logo, and items in self.options, highlighting the currently chosen
    def loop(self, flip=True, handlekeys = True):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, (80, 30))
        self.age +=0.15

        if handlekeys == True:
            esc_pressed = self.handle_keys()
            if esc_pressed == False:
                return False

        y = 250
        x = self.left_margin
        i = 0
        max_len = 0
        #Calculate the longest option to center them
        for option in self.options:
            if max_len < len(option):
                max_len = len(option)

        for option in self.options:
            if i==self.chosen_option:
                color = (255,100,100)
                angle = math.sin(self.age)  * 3
                _y = (y + angle * angle)
            else:
                color = (255,255,255)    
                angle = 0
                _y = y

            text = self.font.render(option.center(max_len), 2, (0,0,0,0))
            self.screen.blit(text, (x, _y+2))
            text = self.font.render(option.center(max_len), 2, color)
            self.screen.blit(text, (x, _y))
            y += self.line_height
            i += 1
        if flip == True:
            pygame.display.flip()


class Menu(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.options = [ "Start game", "Options", "Highscores", "About", "Quit" ]

class Options(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.values = { \
            'Difficulty':'Easy',\
            'Music':'On'\
        }
        try:
            self.values = pickle.load(open('options.p', 'rb'))
        except:
            print "Options file not available"
        self.go_back = False

    def handle_keys(self):
        #Handle Input Events
        Abstract_Menu.handle_keys(self)
        for event in self.events:
            if event.type == KEYDOWN:                 
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_RETURN:
                    print "Chosen option "+str(self.chosen_option)
                    self.toggle_option(self.chosen_option)
                if event.key == K_ESCAPE:
                    self.finished = True
        return True

    def loop(self):
        #set options
        self.options = []
        for value in self.values:
            self.options.append('{0}: {1}'.format(value,self.values[value]))
        self.options.append('Back')
        Abstract_Menu.loop(self)
        

    def toggle_option(self, num_option):
        #Difficulty
        if num_option == 0:
            if self.values['Difficulty'] == "Easy":
                self.values['Difficulty'] = "Hard"
            else:
                self.values['Difficulty'] = "Easy"
        #Music
        elif num_option == 1:
            if self.values['Music'] == "On":
                self.values['Music'] = "Off"
            else:
                self.values['Music'] = "On"
        elif num_option == 2:
            self.finished = True
        pickle.dump(self.values, open('options.p', 'wb'))

#Credits, basically
class About(Abstract_Menu):
    
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.font = utils.load_font('chitown.ttf', 24)
        self.line_height = 40
        self.left_margin = 52
        self.options = [\
            'CREDITS',
            'Game design: kTzAR',
            'Game development: kTzAR',
        ]

    def handle_keys(self):
        #Exit on any key
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                self.finished = True
        return True

class Highscores(Abstract_Menu):
    def __init__(self, screen):
        Abstract_Menu.__init__(self, screen)
        self.font = utils.load_font('chitown.ttf', 24)
        self.line_height = 40
        self.left_margin = 52

        highscores_data = Highscores_data()

        self.highscores = highscores_data.get_highscores()

        self.options = [ 'HIGH-SCORES' ]

        for highscore in self.highscores :
            self.options.append(highscore['name']+': '+str(highscore['score']))

    def handle_keys(self):
        #Only listen to ESC, don't execute parent's handle_keys
        #since there are no options to choose from
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                self.finished = True
        return True

#Ask for a highscore
class Newhighscore(Abstract_Menu):

    def __init__(self, screen, bartending):
        Abstract_Menu.__init__(self, screen)
        self.font           = utils.load_font('chitown.ttf', 24)
        self.font_name      = utils.load_font('chitown.ttf', 30)
        self.player_name    = 'AAA'
        self.bartending     = bartending
        self.any_key_pressed = False
        self.age_2 = 0

        #No options in this menu
        self.options = [ 'New High score', 'You made {0} points'.format(self.bartending.score)]

    def loop(self):
        self.age_2 += 1
        Abstract_Menu.loop(self, False, False)
        text = self.font_name.render(self.player_name, 2, (0,0,0))
        self.screen.blit(text, (52, 302))
        text = self.font_name.render(self.player_name, 2, (255,255,255))
        self.screen.blit(text, (50, 300))
        self.handle_keys()
        pygame.display.flip()

    def handle_keys(self):
        #Only listen to ESC, don't execute parent's handle_keys
        #since there are no options to choose from
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:                 
                #Clean name the first time a key is pressed
                if self.any_key_pressed == False:
                    self.player_name = ''
                    self.any_key_pressed = True
                #convert letter and add it to the name
                try:
                    typed_character = chr(event.key)
                    self.player_name += typed_character
                except:
                    pass

                if event.key == K_RETURN:
                    #TODO store highscore
                    highscores = Highscores_data()
                    print "Save new highscore {0} : {1}".format(self.player_name, self.bartending.score)
                    highscores.set_newhighscore(self.player_name.strip(), self.bartending.score)
                    self.finished = True
                    return True
                #Remove the last character
                if event.key == K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
        return True
