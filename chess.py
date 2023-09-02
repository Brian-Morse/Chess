import pygame
import sys

class Piece(pygame.sprite.Sprite):
    def __init__(self, side, type, pos, has_moved = False):
        super().__init__()
        self.side = side
        self.type = type
        self.pos = pos
        self.has_moved = has_moved
        self.is_clicked = False
        self.image = pygame.image.load(f'images/{side}_{type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = coord_to_pixel(*pos))

    def get_pressure(self):
        pass

    def get_possible_move_locs(self):
        return self.get_pressure()

    def get_move_locs(self):
        pass

    def show_moves(self):
        moves = self.get_move_locs()
        for move in moves:
            screen.blit(avail_move_surf,coord_to_pixel(*move))

    def update(self):
        pass

class Pawn(Piece):
    def __init__(self, side, pos, has_moved = False):
        super().__init__(side, 'pawn', pos, has_moved)

    def get_pressure(self):
        x,y = self.pos
        if self.type == 'white':
            if x == 0:
                return [(1, y-1)]
            elif x == 7:
                return [(6, y-1)]
            else:
                return [(x-1,y-1),(x+1,y-1)]
        else:
            if x == 0:
                return [(1, y+1)]
            elif x == 7:
                return [(6, y+1)]
            else:
                return [(x-1,y+1),(x+1,y+1)]
            
    def get_possible_move_locs(self):
        pressure = self.get_pressure()
        possible_moves = []
        if self.type == 'white':
            for move in pressure:
                if [b_piece for b_piece in black_pieces if b_piece.sprite.pos == move]:
                    possible_moves.append(move)
            

    
                
class Side(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.enpassant = []               


            




SQUARE_SIZE = 80
HEIGHT = 8
WIDTH = 8

def coord_to_pixel(x,y):
    return (x*SQUARE_SIZE,y*SQUARE_SIZE)

#Screen and clock set up
pygame.init()
screen = pygame.display.set_mode((WIDTH*SQUARE_SIZE,HEIGHT*SQUARE_SIZE))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

#Background
board_background = pygame.image.load('images/chess_board.png').convert()

avail_move_surf = pygame.image.load('images/avail_move.png').convert_alpha()

#Pieces set up
white_pieces = Side(Piece('white','rook',(0,7)),Piece('white','knight',(1,7)),
                    Piece('white','bishop',(2,7)),Piece('white','queen',(3,7)),
                    Piece('white','king',(4,7)),Piece('white','rook',(7,7)),
                    Piece('white','knight',(6,7)),Piece('white','bishop',(5,7)))
for x in range(8):
    white_pieces.add(Pawn('white',(x,6)))

black_pieces = Side(Piece('black','rook',(0,0)),Piece('black','knight',(1,0)),
                    Piece('black','bishop',(2,0)),Piece('black','queen',(3,0)),
                    Piece('black','king',(4,0)),Piece('black','rook',(7,0)),
                    Piece('black','knight',(6,0)),Piece('black','bishop',(5,0)))
for x in range(8):
    black_pieces.add(Pawn('black',(x,1)))


for piece in white_pieces:
    print(piece.pos)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(board_background, (0,0))

    white_pieces.update()
    white_pieces.draw(screen)
    
    black_pieces.update()
    black_pieces.draw(screen)

    pygame.display.update()
    clock.tick(60)