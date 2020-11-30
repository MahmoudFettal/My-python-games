# written by Mahmoud Fettal
# in 11/29/2020 (29/11/2020)

#--------------------------------------- import phase ---------------------------------------#

from grid import Grid,Settings # we don't need the full module

import pygame, sys # pygame to define images in the dict of images

#------------------------------------------- class ------------------------------------------#

class Game():

    def __init__(self):
        self.grid  = Grid()
        self.ended = False

    def update(self,screen):
        for i in range(4):
            for j in range(4):
                screen.blit(Settings.colors_imgs[self.grid.grid[i][j].value],(Settings.width * j, Settings.width * i))
        clock = pygame.time.Clock()
        clock.tick(5)
        pygame.display.flip()

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

    def play(self):
        print('welcome! to 2048 build by smauj')
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
                print(f'Game, Over!, your score was {self.grid.score}')
                break
            print(f' move {self.grid.move} '.center(len(f'your score is {self.grid.score}')))
            print(f'your score is {self.grid.score}')
            self.update(screen)
            self.grid.move += 1
        print('Good Bye, see you next time!')

if __name__ == "__main__":
    game = Game()
    game.play()