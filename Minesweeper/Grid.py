from random import randint

class Cell():
    def __init__(self):
        self.contact = 0 # the number of mines in contacts with this cell
        self.mine    = False
        self.covered = True 
    def __repr__(self):
        if self.covered:
            return str(self.contact)
        return 'X'

class Grid():
    def __init__(self, lines, columns, n_mines):
        self.lines   = lines
        self.columns = columns
        self.n_mines = n_mines # the number of mines
        self.r_mines = lines*columns - n_mines # the number of the remainging free cells
        self.grid    = [[Cell() for _ in range(columns)] for _ in range(lines)]

    def fill_mines(self):
        self.mines   = []
        while len(self.mines) < self.n_mines:
            while True:
                x,y = randint(0, self.lines-1), randint(0, self.column-1)
                if not self.grid[x][y] in self.mines:
                    self.mines.append([x,y])
                    break
        
