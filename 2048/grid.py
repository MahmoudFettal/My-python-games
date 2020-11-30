# written by Mahmoud Fettal
# in 11/27/2020 (27/11/2020) 

#--------------------------------------- description ---------------------------------------#

'''
This module contains the building blocks of the game 2048
It contains :
        1- "Settings" class here i store all the general variables so i can change them inside 
    the class without needing to change them all over the code.
        2- "Cell" is the class that contians the value of the cell and the operations between 
    cells.
        3- "Grid" the grid is the main subject of this module and it is the only one used 
    outside it, it contains 4*4 grid of cells and it contains all the methodes for swiping and 
    cheking available cells. 
'''

#--------------------------------------- import phase ---------------------------------------#

from random import randint, choice # we don't need the full module

import pygame, os # pygame to define images in the dict of images

#----------------------------------------- functions ----------------------------------------#

def possibility():
    '''
        the possibility functions gives the value to add based on the possibility of 10 percent of 
    4 and 90 to have 2.
        I used randint to make the possibility it is not 100 accurete.
    '''
    x = randint(1,100)
    if x <= 10:
        return 4
    return 2

def frames_path(x):
    '''
        this function create the path using os.path.join to avoid problems in other os systems
    '''
    return os.path.join('frames',f'{x}.png')

#------------------------------------------- class ------------------------------------------#

class Settings():

    bg_color       = pygame.Color('#fdfffc')
    width          = 128
    window_size    = [width*4 + 3, width*4 + 3]
    colors_imgs    = {2**i: pygame.image.load(frames_path(2**i)) for i in range(1,12)}
    colors_imgs[0] = pygame.image.load(frames_path(0)) 

class Cell():

    def __init__(self,value):
        self.value = value
    
    def merge(self,cell_2):
        self.value  += cell_2.value
        cell_2.value = 0

class Grid():

    def __init__(self):
        self.score = 0
        self.ended = False
        self.move  = 1
        self.grid  = [[Cell(0) for _ in range(4)] for _ in range(4)]

    def empty_cells(self):
        empty = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j].value == 0:
                    empty.append((i,j))
        return empty

    def fill_empty(self):
        empty = self.empty_cells()
        cell  = choice(empty)
        self.grid[cell[0]][cell[1]].value = possibility()
    
    def swap_zero(self,move):
        moves = [[i, i+1] for i in range(3)]
        codes = {'r':['+','k'],'l':['-','k'],'d':['+','f'],'u':['-','f']}
        flip  = {'k': lambda x,y : (x, y), 'f': lambda x,y : (y, x)}
        swips = 0

        direction, way = codes[move]
        if direction == '+':
            moves = moves[::-1]
        while True:
            zero_sawp = 0
            for x in range(4):
                for move in moves:
                    a,b = flip[way](x, move[0])
                    n,m = flip[way](x, move[1])
                    if self.grid[n][m].value == 0 and  self.grid[a][b].value != 0  and direction == '+':
                        swips += 1
                        zero_sawp += 1
                        self.grid[a][b].value, self.grid[n][m].value = self.grid[n][m].value, self.grid[a][b].value
                    if self.grid[a][b].value == 0 and  self.grid[n][m].value != 0  and direction == '-':
                        swips += 1
                        zero_sawp += 1
                        self.grid[a][b].value, self.grid[n][m].value = self.grid[n][m].value, self.grid[a][b].value
            if zero_sawp == 0:
                break
        return swips        
        
    def make_move(self, the_move):
        moves = [[i, i+1] for i in range(3)]
        codes = {'r':['+','k'],'l':['-','k'],'d':['+','f'],'u':['-','f']}
        flip  = {'k': lambda x,y : (x, y), 'f': lambda x,y : (y, x)}
        swips = 0

        direction, way = codes[the_move]
        if direction == '+':
            moves = moves[::-1]
        
        swips += self.swap_zero(the_move)

        for x in range(4):
            i = 0
            while i < 3:
                a,b = flip[way](x, moves[i][0])
                n,m = flip[way](x, moves[i][1])
                if self.grid[a][b].value == 0:
                    pass
                elif self.grid[a][b].value == self.grid[n][m].value or self.grid[n][m].value == 0:
                    if self.grid[a][b].value != 0 and self.grid[m][n].value != 0:
                        i += 1
                    self.score += self.grid[a][b].value + self.grid[n][m].value
                    if direction == '-':
                        self.grid[a][b].merge(self.grid[n][m])
                    else:
                        self.grid[n][m].merge(self.grid[a][b])
                    swips += 1
                i += 1

        swips += self.swap_zero(the_move)

        return swips

    def swips_test(self,i,j,move):
        if self.grid[i][j].value == 0:
            return False
        tests = [(i,j+1),(i,j-1),(i+1,j),(i-1,j)]
        for coords in tests:        
            x,y = coords
            if x in range(4) and y in range(4):
                if self.grid[i][j].value == self.grid[x][y].value:
                    return True
        return False

    def game_over(self):
        for i in range(4):
            for j in range(4):
                if self.swips_test(i,j):
                    return False
        return True

if __name__ == '__main__':
    game = Grid()
    print(game.make_move('l'))
    print(game.make_move('u'))
    print(game.make_move('d'))
    print(game.make_move('r'))
