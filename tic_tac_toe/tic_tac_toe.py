'''
by mahmoud fettal in the 12/25/2020
'''

import pygame,sys,os

class Settings():
    screen_size = (400,500)
    width       = 100
    frames      = {i: pygame.image.load(os.path.join('frames', f'{i}.png')) for i in 'X,O,E,grid,Draw,O to play,X to play,reset,title,X wins,O wins'.split(',')}
    bg_color    = pygame.Color('#FFFFFF')

class Grid():
    def __init__(self):
        self.x_cells   = set()
        self.o_cells   = set()
        self.the_round = 1
        self.ended     = False

    def win_check(self):
        ''' this function checks if the player that played this round won or not
        -ouput:
        returns True if the player won or not
        '''
        
        player_cells = self.x_cells if self.the_round%2 == 1 else self.o_cells

        lines   = [(1+(i*3), 2+(i*3), 3+(i*3)) for i in range(3)]
        columns = [(i, i+3 , i+6) for i in range(1,4)]
        diags   = [(1,5,9),(7,5,3)]

        win_postions = [set(position) for layout in [lines, columns, diags] for position in layout]

        for position in win_postions:
            if position.issubset(player_cells):
                player = 'X' if self.the_round%2 == 1 else 'O'
                self.ended = True 
                return f'{player} wins'


        if self.the_round == 9:
            self.ended = True 
            return 'Draw'

class Tic_tac_toe():
    def __init__(self):
        self.game     = Grid()
        self.settings = Settings()
        self.winner   = 'Draw'
        

    def turn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                n,m = pygame.mouse.get_pos()
                n = (n-50)//100
                m = (m-125)//100
                x = m*3 + n + 1
                if 0 <= n < 3 and 0 <= m < 3 and (not x in self.game.x_cells and not x in self.game.o_cells) :
                    if self.game.the_round % 2 == 1:
                        self.game.x_cells.add(x)
                    else:
                        self.game.o_cells.add(x)

                    self.winner = self.game.win_check()
                    self.game.the_round += 1

    def update(self,screen):
        def frame(x):
            if x in self.game.x_cells:
                return 'X'
            elif x in self.game.o_cells:
                return 'O'
            else:
                return 'E'

        screen.fill(self.settings.bg_color)
        
        screen.blit(self.settings.frames['title'], (106, 24))       

        for i in range(3):
            for j in range(3):
                x = i*3 + j + 1
                screen.blit(self.settings.frames[frame(x)], (50 + j*self.settings.width, 125 + i*self.settings.width))    

        screen.blit(self.settings.frames['grid'], (50,125))
        if self.game.ended:
            screen.blit(self.settings.frames[self.winner], (50,455))
            screen.blit(self.settings.frames['reset'], (301,439))
            self.game_over()

        turn = 'X to play' if self.game.the_round%2 == 1 else 'O to play'
        screen.blit(self.settings.frames[turn], (150, 75))   

        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.flip()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                n,m = pygame.mouse.get_pos()
                if 300 <= n <= 430 and 439 <= m <= 489 :
                    self.play()

    def play(self):
        self.game = Grid()
        pygame.init()
        pygame.display.set_caption('tic tac toe')
        screen = pygame.display.set_mode(self.settings.screen_size)
        screen.fill(self.settings.bg_color)
        self.update(screen)
        while self.game.the_round < 11:
            self.turn()
            self.update(screen)



if __name__ == '__main__':
    tic_tac_toe = Tic_tac_toe()
    tic_tac_toe.play()