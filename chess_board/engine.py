import sys,os,pygame

class Settings():
    screen_size = (1000,1000)
    width       = 100
    frames      = {i: pygame.image.load(os.path.join('frames', f'{i}.png')) for i in '0 1 2 bb border bw kb nb kw nw pb pw qb qw rb rw'.split()}
    bg_color    = pygame.Color('#FFFFFF')

class Piece():
    def __init__(self, position, color, number, p_type):
        self.position = position 
        self.color    = color    
        self.number   = number   
        self.type     = p_type   

    def moves(self):
        x,y  = self.position
        pown = []
        if self.type == 'p':
            if self.position[0] == 1 and self.color == 'w':
                pown = [[[1,0],[2,0]]]
            elif self.position[0] == 6 and self.color == 'b':
                pown = [[[-1,0],[-2,0]]]
            else:
                pown = [[[1 if self.color == 'w' else -1,0]]]
        directions = {'up'    : [[i,0] for i in range(1,8)],
                      'down'  : [[-i,0] for i in range(1,8)],
                      'right' : [[0,i] for i in range(1,8)],
                      'left'  : [[0,-i] for i in range(1,8)],
                      'upl'   : [[i,-i] for i in range(1,8)],
                      'downl' : [[-i,-i] for i in range(1,8)],
                      'upr'   : [[i,i] for i in range(1,8)],
                      'downr' : [[-i,i] for i in range(1,8)]} 

        piece_moves = {'k' : [[[i,j]] for i in [-1, 1] for j in [-1, 1]] + [[[0,1],[0,-1],[1,0],[-1,0]]],
                       'p' : pown,
                       'n' : [[[i,j],[j,i]] for i in [1,-1] for j in [2,-2]]  ,     
                       'q' : [directions[i] for i in 'up down right left upl downl upr downr'.split()],
                       'r' : [directions[i] for i in 'up down right left'.split()],   
                       'b' : [directions[i] for i in 'upl downl upr downr'.split()] ,    
                      } 

        possible = [[[coor[0] + x, coor[1] + y] for coor in direction if (0 <= coor[0] + x < 8 and 0 <= coor[1] + y < 8)] for direction in piece_moves[self.type ]]
        return possible
        
    def __repr__(self):
        result = self.type if self.color == 'w' else self.type.upper()
        if self.type == 'ki':
            return result
        return result+str(self.number)

class Board():
    def __init__(self):
        self.pieces = {}
        self.board  = [['' for _ in range(8)] for _ in range(8)]
    
    def start(self):
        ids    = {i: 1 for i in 'r b n q k'.split()}
        for i,j in enumerate('r n b k q b n r'.split()): 
            white_piece, black_piece = Piece((0,i), 'w', ids[j], j), Piece((7,i), 'b', ids[j], j)
            white_pown , black_pown  = Piece((1,i), 'w', i+1, 'p'), Piece((6,i), 'b', i+1, 'p')
            self.pieces[str(white_piece)] = white_piece
            self.pieces[str(black_piece)] = black_piece
            self.pieces[str(white_pown)] = white_pown
            self.pieces[str(black_pown)] = black_pown
            ids[j] += 1
        for piece in self.pieces:
            x,y = self.pieces[piece].position
            self.board[x][y] = str(self.pieces[piece])

    def showmoves(self,piece_code):
        piece = self.pieces[piece_code]
        possible_moves = piece.moves()
        p_moves  = []
        if piece.type in 'kn':
            possible_moves = [i for j in possible_moves for i in j]
            for x,y in possible_moves:
                if self.board[x][y] == '' or self.pieces[self.board[x][y]].color != piece.color:
                    p_moves.append([x,y])
        elif piece.type == 'p':
            possible_moves = [i for j in possible_moves for i in j]
            for x,y in possible_moves:
                if self.board[x][y] == '':
                    p_moves.append([x,y])
            a,b  = piece.position
            sign = 1 if piece.color == 'w' else -1 
            if 0 <= a+sign < 8 and 0 <= b+1 < 8 and self.board[a+sign][b+1] != '' and self.pieces[self.board[a+sign][b+1]].color != piece.color:
                p_moves.append([a+sign,b+1])
            if 0 <= a+sign < 8 and 0 <= b-1 < 8 and self.board[a+sign][b-1] != '' and self.pieces[self.board[a+sign][b-1]].color != piece.color:
                p_moves.append([a+sign,b-1])
        else:
            for direction in possible_moves:
                for x,y in direction:
                    if self.board[x][y] == '':
                        p_moves.append([x,y])
                    elif self.pieces[self.board[x][y]].color != piece.color:
                        p_moves.append([x,y])
                        break
                    else:
                        break
        return p_moves  

    def move(self, piece_code, direction):
        x,y = direction
        piece = self.pieces[piece_code]
        self.pieces.pop(self.board[x][y],None)
        piece.position = (x,y)
        self.pieces[piece_code] = piece          
        self.board  = [['' for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            x,y = self.pieces[piece].position
            self.board[x][y] = str(piece)
