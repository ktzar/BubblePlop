#Import Modules
import os, pygame, time
from pygame.locals import *
from stage import *
from menus import *


def BubblePlop():
    pygame.init()
    if not pygame.font: print 'Warning, fonts disabled'
    if not pygame.mixer: print 'Warning, sound disabled'
    screen = pygame.display.set_mode((480, 640), pygame.DOUBLEBUF)
    pygame.display.set_caption('Bubble Plop')
    #pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(1)
#icon
#icon, foo = utils.load_image('icon.png')
#pygame.display.set_icon(icon)

    stage   = Stage(screen)
    menu    = Menu(screen)
    about   = About(screen)
    clock = pygame.time.Clock()

    while 1:
        clock.tick(100)
        if menu.selected_option == -1:
            menu.loop()
        elif menu.selected_option == 0:
            stage.loop()
        elif menu.selected_option == 3:
            about.loop()
        elif menu.selected_option == 4:
            pygame.quit()
            quit()
