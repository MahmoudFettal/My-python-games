# written by Mahmoud Fettal
# in 11/29/2020 (29/11/2020)

#--------------------------------------- import phase ---------------------------------------#

from grid import Cell, Grid, Settings # we don't need the full module

import pygame, sys, os # pygame to define images in the dict of images

#------------------------------------------- class ------------------------------------------#

class Game():

    def __init__(self):
        self.grid  = Grid()
        self.ended = False

    def update(self,screen, over = False):
        screen.fill(Settings.bg_color)
        for i in range(4):
            for j in range(4):
                screen.blit(Settings.colors_imgs[self.grid.grid[i][j].value],(50 + Settings.width * j, 110 + Settings.width * i))
        screen.blit(pygame.image.load(os.path.join('frames','borders.png')), Settings.positions['grid'])
        screen.blit(pygame.image.load(os.path.join('frames','logo.png')), Settings.positions['logo'])
        screen.blit(pygame.image.load(os.path.join('frames','new game.png')), Settings.positions['button'])
        screen.blit(pygame.image.load(os.path.join('frames','background.png')), Settings.positions['score'])
        self.display_score(screen)
        if over:
            screen.blit(pygame.image.load(os.path.join('frames','game_over.png')), Settings.positions['grid'])
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()

    def display_score(self,screen):
        length = 130 + 19*len(str(self.grid.score))
        start  = 140 + (400 - length)/2
        screen.blit(pygame.image.load(os.path.join('frames','score.png')), (start, 749))
        start += 130
        for num in str(self.grid.score):
            screen.blit(pygame.image.load(os.path.join('frames', 'numbers', f'{num}.png')), (start, 749))
            start += 19 

    def get_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_RIGHT:
                    return 'r'
                elif event.key == pygame.K_LEFT:
                    return 'l'
                elif event.key == pygame.K_UP:
                    return 'u'
                elif event.key == pygame.K_DOWN:
                    return 'd'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 460 <= pos[0] <=620 and 35 <= pos[1] <= 75:
                    self.grid = Grid()
                    self.play()

    def play(self):
        #print('welcome! to 2048 build by smauj')
        pygame.init()
        pygame.display.set_caption('2048')

        screen = pygame.display.set_mode(Settings.window_size)

        # the game start here 

        self.grid.fill_empty()
        self.update(screen)

        while True:
            if len(self.grid.empty_cells()) != 0:
                self.grid.fill_empty()
                self.update(screen)

            while True: 
                the_move = self.get_move()
                if len(self.grid.empty_cells()) == 0:
                    if self.grid.game_over():
                        self.ended = True
                        break
                if not(the_move == None) and self.grid.make_move(the_move):
                    break
            if self.ended:
                self.update(screen, True)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if 460 <= pos[0] <=620 and 35 <= pos[1] <= 75:
                                self.grid = Grid()
                                self.ended = False
                                self.play()

            self.update(screen)
            self.grid.move += 1


if __name__ == "__main__":
    game = Game()
    game.play()