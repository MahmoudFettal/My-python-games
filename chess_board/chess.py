from engine import Settings, Board
import pygame,sys

class Chess():
    def update(self,screen):  
        screen.blit(Settings.frames['border'], (75, 75)) 
        for i in range(8):
            for j in range(8):
                screen.blit(Settings.frames[str((i%2 + j%2)%2)], (100 + j*Settings.width, 100 + i*Settings.width)) 
                piece = self.game.board[i][j]
                if piece!= '':
                    piece = self.game.pieces[piece]
                    frame = piece.type + piece.color
                    screen.blit(Settings.frames[frame], (100 + j*Settings.width, 100 + i*Settings.width)) 

        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.flip()

    def show_moves(self,screen,cases):  
        screen.blit(Settings.frames['border'], (75, 75)) 
        for i in range(8):
            for j in range(8):
                if [i,j] in cases:
                    screen.blit(Settings.frames['2'], (100 + j*Settings.width, 100 + i*Settings.width)) 
                else:
                    screen.blit(Settings.frames[str((i%2 + j%2)%2)], (100 + j*Settings.width, 100 + i*Settings.width)) 
                piece = self.game.board[i][j]
                if piece!= '':
                    piece = self.game.pieces[piece]
                    frame = piece.type + piece.color
                    screen.blit(Settings.frames[frame], (100 + j*Settings.width, 100 + i*Settings.width)) 

        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.flip()

    def make_move(self, screen, moves, piece):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                n,m = pygame.mouse.get_pos()
                if 100 <= n <= 900 and 100 <= m <= 900:
                    i,j = n//100 - 1,m//100 - 1  
                    self.played = False                 
                    if [j,i] in moves:
                        self.game.move(piece, [j,i])
                        self.round += 1
                    else:
                        self.turn(screen)

    def turn(self,screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                n,m = pygame.mouse.get_pos()
                if 100 <= n <= 900 and 100 <= m <= 900:
                    i,j = n//100 - 1,m//100 - 1
                    piece = self.game.board[j][i]
                    color = 'w' if self.round%2 == 1 else 'b'
                    if piece != ''  and self.game.pieces[piece].color == color :
                        moves = self.game.showmoves(piece)
                        self.played = True
                        while self.played:
                            self.show_moves(screen, moves)
                            self.make_move(screen, moves, piece)
                        return True

    def play(self):
        self.game = Board()
        self.game.start()
        self.round = 1
        pygame.init()
        pygame.display.set_caption('Chess')
        screen = pygame.display.set_mode(Settings.screen_size)
        screen.fill(Settings.bg_color)
        while True:
            self.update(screen)
            while not self.turn(screen):
                pass
            

if __name__ == '__main__':
    game = Chess()
    game.play()


# bugs need to be fixed:
    # when you click on a case out of the possible moves and it contains a piece it must work with no need of double click