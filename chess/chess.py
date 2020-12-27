import sys

class Piece():
    def __init__(self, position, color, number, p_type):
        self.position = position 
        self.color    = color    
        self.number   = number   
        self.type     = p_type   

    def moves(self):
        x,y = self.position
        directions = {'up'    : [[i,0] for i in range(1,8)],
                      'down'  : [[-i,0] for i in range(1,8)],
                      'right' : [[0,i] for i in range(1,8)],
                      'left'  : [[0,-i] for i in range(1,8)],
                      'upl'   : [[i,-i] for i in range(1,8)],
                      'downl' : [[-i,-i] for i in range(1,8)],
                      'upr'   : [[i,i] for i in range(1,8)],
                      'downr' : [[-i,i] for i in range(1,8)]} 
        piece_moves = {'k' : [[[i,j]] for i in [-1, 1] for j in [-1, 1]],
                       'K' : [[[i,j]] for i in [-1, 1] for j in [-1, 1]], 
                       'p' : [[[1,0]]],
                       'P' : [[[-1,0]]],
                       'n' : [[[i,j],[j,i]] for i in [1,-1] for j in [2,-2]], 
                       'N' : [[[i,j],[j,i]] for i in [1,-1] for j in [2,-2]],      
                       'q' : [directions[i] for i in 'up down right left upl downl upr downr'.split()],
                       'Q' : [directions[i] for i in 'up down right left upl downl upr downr'.split()], 
                       'r' : [directions[i] for i in 'up down right left'.split()],  
                       'R' : [directions[i] for i in 'up down right left'.split()],  
                       'b' : [directions[i] for i in 'upl upr'.split()],  
                       'B' : [directions[i] for i in 'downl downr'.split()],  
                      } 

        side = self.type[0] if self.color == 'w' else self.type.upper()
        possible = [[[coor[0] + x, coor[1] + y] for coor in direction if (0 <= coor[0] + x < 8 and 0 <= coor[1] + y < 8)] for direction in piece_moves[side]]
        return possible
    def __repr__(self):
        result = self.type if self.color == 'w' else self.type.upper()
        if self.type == 'ki' or self.type == 'qu':
            return result
        return result+str(self.number)

class Board():
    def __init__(self):
        self.pieces = {}
        self.board  = [['  ' for _ in range(8)] for _ in range(8)]
    
    def initialize(self):
        ids    = {i: 1 for i in 'r b n qu ki'.split()}
        for i,j in enumerate('r n b qu ki b n r'.split()): 
            white_piece, black_piece = Piece((0,i), 'w', ids[j], j), Piece((7,i), 'b', ids[j], j)
            white_pown , black_pown  = Piece((1,i), 'w', i+1, 'p'), Piece((6,i), 'b', i+1, 'p')
            self.pieces[str(white_piece)] = white_piece
            self.pieces[str(black_piece)] = black_piece
            self.pieces[str(white_pown)] = white_pown
            self.pieces[str(black_pown)] = black_pown
            ids[j] += 1

    def showmoves(self,piece_code):
        piece = self.pieces[piece_code]
        possible_moves = piece.moves()
        p_moves  = []
        output = ''
        coord  = 'abcdefgh'
        if piece.type in 'p ki n':
            possible_moves = [i for j in possible_moves for i in j]
            for x,y in possible_moves:
                if self.board[x][y] == '  ' or self.pieces[self.board[x][y]].color != piece.color:
                    output += coord[y] + str(x+1) + ' '
                    p_moves.append([x,y])
        else:
            for direction in possible_moves:
                for x,y in direction:
                    if self.board[x][y] == '  ':
                        output += coord[y] + str(x+1) + ' '
                        p_moves.append([x,y])
                    elif self.pieces[self.board[x][y]].color != piece.color:
                        output += coord[y] + str(x+1) + ' '
                        p_moves.append([x,y])
                        break
                    else:
                        break
        if output == '':
            return p_moves,'FAILED'
        else:
            return p_moves,output  

    def move(self, piece_code, direction):
        x,y   = int(direction[1])-1,list('abcdefgh').index(direction[0])
        piece = self.pieces[piece_code]
        possible_moves = self.showmoves(piece_code)[0]
        if [x,y] in possible_moves:
            self.pieces.pop(self.board[x][y],None)
            piece.position = (x,y)
            self.pieces[piece_code] = piece   

            print('OK')             
        else:
            if piece.type == 'p':
                if [x,y] == [piece.position[0] + piece.sign, piece.position[1]+1] or [x,y] == [piece.position[0] + piece.sign, piece.position[1]-1]:
                    print(self.board[x][y],[x,y])
                    if self.board[x][y] != '  ' and self.pieces[self.board[x][y]].color != piece.color:
                        del self.pieces[self.board[x][y]]
                        piece.position = (x,y)
                        self.pieces[piece_code] = piece    
                        print('OK')      
                    else:
                        print('FAILED')          
                else:
                    print('FAILED')
            else:
                print('FAILED')
        self.board  = [['  ' for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            x,y = self.pieces[piece].position
            self.board[x][y] = str(piece)

    def show(self):
        self.board  = [['  ' for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            x,y = self.pieces[piece].position
            self.board[x][y] = str(piece)
        print('-------------------------')
        print('\n'.join(' '.join(i) for i in self.board)[::-1])
        print('-------------------------')

f = open(sys.argv[1],'r')
commands = [[line.split()] for line in f.readlines()]
f.close()

chess = Board()
chess.initialize()

for command in commands:
    command = command[0]
    print('>',' '.join(command))
    if command[0] == 'initialize':
        chess.initialize()
        print('ok')
        chess.show()
    elif command[0] == 'showmoves':
        print(chess.showmoves(command[1])[1])
    elif command[0] == 'move':
        chess.move(command[1],command[2])
    elif command[0] == 'print':
        chess.show()
    elif command[0] == 'exit':
        break