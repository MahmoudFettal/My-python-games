from grid import Cell, Grid, Settings # we don't need the full module

import pygame, sys, os # pygame to define images in the dict of images

#------------------------------------------- class ------------------------------------------#

class Game():
    def __init__(self,lines,columns,mines):
        self.grid     = Grid(lines,columns,mines)
        self.lines    = lines
        self.columns  = columns
        self.settings = Settings(self.lines,self.columns)

    def update(self,screen):
        for i in range(self.grid.lines):
            for j in range(self.grid.columns):
                screen.blit(self.settings.frames[str(self.grid.grid[i][j])], (j*105,i*105))
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()
        
    def get_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                n,m = pygame.mouse.get_pos()
                self.grid.make_move(m//105,n//105)
                self.grid.show()

    def play(self):
        pygame.init()
        pygame.display.set_caption('minesweeper')
        screen = pygame.display.set_mode(self.settings.screen_size)
        self.grid.fill_mines()
        self.grid.mines_contact()
        self.update(screen)
        while True:
            self.get_move()
            self.update(screen)
            

if __name__ == "__main__":
    game = Game(5,5,5)
    game.play()