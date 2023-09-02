import pygame
import sys

class Piece(pygame.sprite.Sprite):
    def __init__(self, side, type, pos, has_moved = False):
        super().__init__()
        self.side = side
        self.type = type
        self.pos = pos
        self.has_moved = has_moved
        self.image = pygame.image.load(f'images/{side}_{type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = coord_to_pixel(*pos))

    def update(self):
        screen.blit(avail_move_surf,coord_to_pixel(*self.pos))




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

#TEMPORARY SET UP FOR TESTING
white_pieces = []
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','rook',(0,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','knight',(1,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','bishop',(2,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','queen',(3,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','king',(4,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','rook',(7,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','knight',(6,7))))
white_pieces.append(pygame.sprite.GroupSingle(Piece('white','bishop',(5,7))))
for x in range(8):
    white_pieces.append(pygame.sprite.GroupSingle(Piece('white','pawn',(x,6))))

black_pieces = []
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','rook',(0,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','knight',(1,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','bishop',(2,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','queen',(3,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','king',(4,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','rook',(7,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','knight',(6,0))))
black_pieces.append(pygame.sprite.GroupSingle(Piece('black','bishop',(5,0))))
for x in range(8):
    black_pieces.append(pygame.sprite.GroupSingle(Piece('black','pawn',(x,1))))






while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(board_background, (0,0))
    for piece in white_pieces:
        piece.draw(screen)
        piece.update()
    for piece in black_pieces:
        piece.draw(screen)

    pygame.display.update()
    clock.tick(60)