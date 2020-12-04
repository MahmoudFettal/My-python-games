from random import randint
import pygame, os

class Settings():
    def _init_(self, lines, columns):
        self.lines   = lines
        self.columns = columns
        self.screen_size = (21*self.lines, 21*self.columns) 
        self.frames      = {frame : pygame.image.load(os.path.join('frames',f'{frame}.png')) for frame in ['U'] + list(map(str,range(9)))}

class Cell():
    def __init__(self):
        self.contact = 0 # the number of mines in contacts with this cell
        self.mine    = False
        self.covered = False 
    def __repr__(self):
        if self.covered:
            return str(self.contact)
        return 'U'

class Grid():
    def __init__(self, lines, columns, n_mines):
        self.lines   = lines
        self.columns = columns
        self.n_mines = n_mines # the number of mines
        self.r_cells = lines*columns - n_mines # the number of the remainging free cells
        self.grid    = [[Cell() for _ in range(columns)] for _ in range(lines)]
        self.zeros   = []
        self.over    = False

    def fill_mines(self):
        self.mines   = []
        while len(self.mines) < self.n_mines:
            while True:
                x,y = randint(0, self.lines-1), randint(0, self.columns-1)
                if not [x,y] in self.mines:
                    self.grid[x][y].mine = True
                    self.mines.append([x,y])
                    break

    def neighbours(self,i,j):
        self.coords = [[-1, -1],[-1, 0], [-1, 1],
                  [ 0, -1],         [0, 1 ],
                  [ 1, -1], [1, 0], [1, 1 ]]
        for x,y in self.coords:
            x,y = i+x,j+y
            if 0 <= x < self.lines and 0 <= y < self.columns and not self.grid[x][y].mine:
                self.grid[x][y].contact += 1

    def mines_contact(self):
        for i,j in self.mines: 
            self.neighbours(i,j)

    def uncover(self,i,j):
        if not self.grid[i][j].covered:
            self.r_cells -= 1
            self.grid[i][j].covered = True 
            if self.grid[i][j].contact == 0:
                self.zeros.append((i,j))
                for a,b in self.coords:
                    if 0 <= a+i < self.lines and 0 <= b+j < self.columns and not self.grid[a+i][b+j].mine and not (a+i,b+j) in self.zeros:
                        self.uncover(a+i, b+j)
    
    def make_move(self,x,y):
        '''while True:
            x,y = map(int, input().split())
            if 0 <= x < self.lines and 0 <= y < self.columns and not self.grid[x][y].covered:
                break  '''
        if self.grid[x][y].mine:
            self.over = True
        else:    
            self.uncover(x,y)

    def show(self):
        self.mines_contact()
        print('\n'.join([' '.join([str(j.contact) for j in i]) for i in self.grid]))    
        print('\n'.join([' '.join(list(map(str,i))) for i in self.grid])) 
        while not self.over:
            self.make_move()
            print('\n'.join([' '.join(list(map(str,i))) for i in self.grid])) 
        print('game over')
 
if __name__ == "__main__":
    game = Grid(5,5,5)
    game.fill_mines()
    game.show()