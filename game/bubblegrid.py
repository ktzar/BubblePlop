import os, pygame
from pygame.locals import *
from sprites import Bubble
import utils

class Bubblegrid():

    def __init__(self, width, height, spritegroup):
        self.debug = False
        self.grid_size  = (width,height)
        self.bubbles    = spritegroup
        self.bubbles_grid = []
        self.bubble_size    = (32,32)
        self.bubble_offsets = (50,100)
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

    def print_grid(self):
        output = ""
        for j in range(self.grid_size[1]):
            for i in range(self.grid_size[0]):
                if self.bubbles_grid[i][j] != False:
                    output = "{0}{1}".format(output, self.bubbles_grid[i][j].value)
                else:
                    output += "X"

            output += "\n"
        print output

    def column_fall(self, x,y):
        for i in range(y):
            _y = y-i
            if self.debug : print "fall ",_y
            if self.bubbles_grid[x][_y-1] == False:
                self.bubbles_grid[x][_y] = False
            else:
                self.bubbles_grid[x][_y] = self.bubbles_grid[x][_y-1]
                #self.bubbles_grid[x][_y].rect.top += self.bubble_size[1]
                self.bubbles_grid[x][_y].move_down()
        self.bubbles_grid[x][0] = False

    def process_holes(self):
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                #From bottom to top
                _y = self.grid_size[1] - y - 1
                if self.bubbles_grid[x][_y] == False:
                    if self.debug:print "Column fall {0},{1}".format(x,_y)
                    self.column_fall(x,_y)

    def find_surrounding(self,x,y,rec=0):
        if rec > 6:
            return []
        matched = [[x,y]]
        try:
            #Check the surounding bubbles if the current is not in the border
            #top
            if y>0 and self.bubbles_grid[x][y-1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x,y-1, rec+1)
                for ret in returned:
                    matched.append(ret)
            #Bottom
            if y<self.grid_size[1]-1 and self.bubbles_grid[x][y+1].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x,y+1, rec+1)
                for ret in returned:
                    matched.append(ret)
            #Right
            if x < self.grid_size[0] and self.bubbles_grid[x+1][y].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x+1,y, rec+1)
                for ret in returned:
                    matched.append(ret)
            #Left
            if x > 0 and self.bubbles_grid[x-1][y].value == self.bubbles_grid[x][y].value:
                returned = self.find_surrounding(x-1,y, rec+1)
                for ret in returned:
                    matched.append(ret)
            #If the column is even, check on the sides' top corners of the current bubble
            if x%2 == 0:
                if self.bubbles_grid[x-1][y-1].value == self.bubbles_grid[x][y].value:
                    returned = self.find_surrounding(x-1,y-1, rec+1)
                    for ret in returned:
                        matched.append(ret)
                if self.bubbles_grid[x+1][y-1].value == self.bubbles_grid[x][y].value:
                    returned = self.find_surrounding(x+1,y-1, rec+1)
                    for ret in returned:
                        matched.append(ret)
            #If the column is odd, check on the sides' bottom corners of the current bubble
            else:
                if self.bubbles_grid[x-1][y+1].value == self.bubbles_grid[x][y].value:
                    returned = self.find_surrounding(x-1,y+1, rec+1)
                    for ret in returned:
                        matched.append(ret)
                if self.bubbles_grid[x+1][y+1].value == self.bubbles_grid[x][y].value:
                    returned = self.find_surrounding(x+1,y+1, rec+1)
                    for ret in returned:
                        matched.append(ret)
        except:
            #This is normal, there will be some attemps to access non-existing values in the grid
            pass
        matched = utils.unique(matched)
        if self.debug:print "matched"
        if self.debug:print matched
        return matched

    def process_click(self,pos):
        exploded = []
        pos_x = (pos[0]-self.bubble_offsets[0]) / self.bubble_size[0]

        #clicks in even columns need to be shifted half a bubble's size
        offset_y = ((pos_x)%2) *(self.bubble_size[1]/2)
        if self.debug:print offset_y

        pos_y = (pos[1]-self.bubble_offsets[1]-offset_y) / self.bubble_size[1]

        if  pos_x < 0 or pos_x > self.grid_size[0]-1 or \
                pos_y < 1 or pos_y > self.grid_size[1]-1:
            if self.debug:print "Aim better mate"
        else:
            if self.debug: print "{0}:{1}".format(pos_x,pos_y)
            surrounding_bubbles = self.find_surrounding(pos_x,pos_y)
            #surrounding_bubbles = [[pos_x,pos_y]]
            for surrounding_bubble in surrounding_bubbles:
                if self.bubbles_grid[surrounding_bubble[0]][surrounding_bubble[1]] != False:
                    exploded.append(self.bubbles_grid[surrounding_bubble[0]][surrounding_bubble[1]].rect)
                    self.bubbles_grid[surrounding_bubble[0]][surrounding_bubble[1]].kill()#.rect.left = 0
                    self.bubbles_grid[surrounding_bubble[0]][surrounding_bubble[1]] = False
                self.process_holes()
            if self.debug: print_grid()
        return exploded

