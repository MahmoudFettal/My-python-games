from grid import Cell, Grid, Settings # we don't need the full module

import pygame, sys, os # pygame to define images in the dict of images

#------------------------------------------- class ------------------------------------------#

class Game():
    def __init__(self,lines,columns,mines):
        self.grid     = Grid(lines,columns,mines)
        self.lines    = lines
        self.columns  = columns
        self.settings = Settings(self.lines,self.columns)
        self.mines    = mines

    def update(self,screen):
        for i in range(self.grid.lines):
            for j in range(self.grid.columns):
                screen.blit(self.settings.frames[str(self.grid.grid[i][j])], (10 + j*self.settings.width, 50 + i*self.settings.width))   
        screen.blit(self.settings.frames['playing'], (10+(self.grid.columns-1)*self.settings.width, 12))        
        self.display_score(screen)
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()

    def game_over(self,screen):
        for i in range(self.grid.lines):
            for j in range(self.grid.columns):
                if [i,j] in self.grid.mines:
                    screen.blit(self.settings.frames['M'], (10 + j*self.settings.width,50 + i*self.settings.width))
                else:
                    screen.blit(self.settings.frames[str(self.grid.grid[i][j].contact)], (10 + j*self.settings.width,50 + i*self.settings.width))
        screen.blit(self.settings.frames['lost'], (10+(self.grid.columns-1)*self.settings.width, 12))                
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()

    def game_won(self,screen):
        for i in range(self.grid.lines):
            for j in range(self.grid.columns):
                if [i,j] in self.grid.mines:
                    screen.blit(self.settings.frames['M'], (10 + j*self.settings.width,50 + i*self.settings.width))
                else:
                    screen.blit(self.settings.frames[str(self.grid.grid[i][j].contact)], (10 + j*self.settings.width,50 + i*self.settings.width))
        screen.blit(self.settings.frames['won'], (10+(self.grid.columns-1)*self.settings.width, 12))                
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()

    def get_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                n,m = pygame.mouse.get_pos()
                if 50 < m < 50+(self.grid.columns)*self.settings.width and 10 < n < 10 + (self.grid.columns)*self.settings.width:
                    self.grid.make_move((m-50)//self.settings.width,(n-10)//self.settings.width)
                elif 10 + (self.grid.columns-1)*self.settings.width <= n <= (self.grid.columns-1)*self.settings.width + 36 and 12 <= m < 38:
                    self.grid = Grid(self.lines, self.columns, self.mines)
                    self.play()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                n,m = pygame.mouse.get_pos()
                if m > 50 or m < (self.grid.columns)*self.settings.width or n > 10 or n < (self.grid.columns)*self.settings.width:
                    if self.grid.grid[(m-50)//self.settings.width][(n-10)//self.settings.width].flaged:
                        self.grid.grid[(m-50)//self.settings.width][(n-10)//self.settings.width].flaged = False
                        self.grid.c_flaged -= 1
                    else:
                        self.grid.grid[(m-50)//self.settings.width][(n-10)//self.settings.width].flaged = True
                        self.grid.c_flaged += 1

    def display_score(self,screen):
        screen.blit(pygame.image.load(os.path.join('frames','block.png')), (10, 12))
        num = str(self.grid.n_mines - self.grid.c_flaged)
        if len(num) == 1:
            screen.blit(pygame.image.load(os.path.join('frames', 'numbers', '0.png')), (19, 18))
            screen.blit(pygame.image.load(os.path.join('frames', 'numbers', f'{num}.png')), (34, 18))
        else:
            screen.blit(pygame.image.load(os.path.join('frames', 'numbers', f'{num[0]}.png')), (19, 18))
            screen.blit(pygame.image.load(os.path.join('frames', 'numbers', f'{num[1]}.png')), (34, 18))

    def play(self):
        pygame.init()
        pygame.display.set_caption('minesweeper')
        screen = pygame.display.set_mode(self.settings.screen_size)
        screen.fill(self.settings.bg_color)
        self.grid.fill_mines()
        self.grid.mines_contact()
        self.update(screen)
        while True:
            self.get_move()
            self.update(screen)
            if self.grid.over:
                self.game_over(screen)
                while True:
                    self.get_move()
            elif self.grid.won:
                self.game_won(screen)
                while True:
                    self.get_move()            

if __name__ == "__main__":
    game = Game(16,16,40)
    game.play()