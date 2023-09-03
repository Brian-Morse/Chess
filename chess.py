import pygame
import sys

class Piece(pygame.sprite.Sprite):
    """Sprite class to represent all possible chess pieces"""
    def __init__(self, side, type, pos, has_moved = False):
        """Initiates the general chess piece"""
        super().__init__()
        self.side = side
        self.type = type
        self.pos = pos
        self.has_moved = has_moved
        self.is_clicked = False
        self.image = pygame.image.load(f'images/{side}_{type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = coord_to_pixel(*pos))

    def get_pressure(self):
        """Returns the positions that this chess piece puts pressure on"""
        pass

    def get_possible_move_locs(self):
        """Returns the possible move locations, ignoring check"""
        return self.get_pressure()

    def get_move_locs(self):
        """Returns locations this piece can move to"""
        return self.get_possible_move_locs()

    def show_moves(self):
        """Visualize the locations the chess piece can move to"""
        moves = self.get_move_locs()
        for move in moves:
            screen.blit(avail_move_surf,coord_to_pixel(*move))

    def update(self, events):
        """Update the chess piece action and visual"""
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    #This piece is already clicked
                    if self.is_clicked:
                        #Clicking the same piece
                        if self.pos == pixel_to_coord(*event.pos):
                            self.is_clicked = True
                        #Check for other possibilities and take action
                        else:
                            self.is_clicked = False
                    else:
                        #See if the piece is being clicked for the first time
                        if self.pos == pixel_to_coord(*event.pos):
                            self.is_clicked = True

        if self.is_clicked:
            #TEMPORARY
            #Visual continuance
            screen.blit(avail_move_surf,coord_to_pixel(*self.pos))
            self.show_moves()


class Pawn(Piece):
    """Creates a Pawn chess piece, most common piece from chess"""
    def __init__(self, side, pos, has_moved = False):
        """Initiates the Pawn piece"""
        super().__init__(side, 'pawn', pos, has_moved)

    def get_pressure(self):
        """Returns the diagonal points of applied pressure"""
        x,y = self.pos
        if self.side == 'white':
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
        """Sees if there are pieces to take diagonally or space ahead"""
        pressure = self.get_pressure()
        possible_moves = []
        if self.side == 'white':
            #Check if there are diagonal points to capture
            for move in pressure:
                if collide_point(black_pieces,*move):
                    possible_moves.append(move)
            #Checks if there is a piece ahead of the pawn
            if (not collide_point(black_pieces, self.pos[0], self.pos[1]-1) and 
                not collide_point(white_pieces, self.pos[0],self.pos[1]-1)):
                
                possible_moves.append((self.pos[0],self.pos[1]-1))
                #Checks if the pawn has moved and if there is a piece two 
                #spaces ahead
                if (not self.has_moved and not 
                    collide_point(black_pieces, self.pos[0], self.pos[1]-2) and 
                    not collide_point(white_pieces, self.pos[0],self.pos[1]-2)):
                    
                    possible_moves.append((self.pos[0],self.pos[1]-2))
        else:
            #Checks if there are diagonal points to capture
            for move in pressure:
                if collide_point(white_pieces,*move):
                    possible_moves.append(move)
            #Checks if there is a piece ahead of the pawn
            if (not collide_point(black_pieces, self.pos[0], self.pos[1]+1) and 
                not collide_point(white_pieces, self.pos[0],self.pos[1]+1)):
                
                possible_moves.append((self.pos[0],self.pos[1]+1))
                #Checks if the pawn has moved and if there is a piece two 
                #spaces ahead
                if (not self.has_moved and not 
                    collide_point(black_pieces, self.pos[0], self.pos[1]+2) and 
                    not collide_point(white_pieces, self.pos[0],self.pos[1]+2)):
                    possible_moves.append((self.pos[0],self.pos[1]+2))
        return possible_moves
                
class Side(pygame.sprite.Group):
    """Group class to hold a player's pieces"""
    def __init__(self, *sprites):
        """Initializes group variables to track game"""
        super().__init__(*sprites)
        self.enpassant = []               

#Constants
SQUARE_SIZE = 80
HEIGHT = 8
WIDTH = 8

def coord_to_pixel(x,y):
    """Returns the pixel location of a provided coordinate"""
    return (x*SQUARE_SIZE,y*SQUARE_SIZE)

def pixel_to_coord(x,y):
    """Returns the coordinate location of a provided pixel"""
    return ((int)(x/SQUARE_SIZE),(int)(y/SQUARE_SIZE))

def collide_point(group,x,y):
    """Returns a list of all pieces that collide with a coordinate"""
    return [piece for piece in group if piece.pos == (x,y)]

#Screen and clock set up
pygame.init()
screen = pygame.display.set_mode((WIDTH*SQUARE_SIZE,HEIGHT*SQUARE_SIZE))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

#Background
board_background = pygame.image.load('images/chess_board.png').convert()

avail_move_surf = pygame.image.load('images/avail_move.png').convert_alpha()

#White pieces set up
white_pieces = Side(Piece('white','rook',(0,7)),Piece('white','knight',(1,7)),
                    Piece('white','bishop',(2,7)),Piece('white','queen',(3,7)),
                    Piece('white','king',(4,7)),Piece('white','rook',(7,7)),
                    Piece('white','knight',(6,7)),Piece('white','bishop',(5,7)))
for x in range(8):
    white_pieces.add(Pawn('white',(x,6)))

# white_pieces.add(Pawn('white',(4,2)))
# white_pieces.add(Pawn('white',(4,3)))

#Black pieces set up
black_pieces = Side(Piece('black','rook',(0,0)),Piece('black','knight',(1,0)),
                    Piece('black','bishop',(2,0)),Piece('black','queen',(3,0)),
                    Piece('black','king',(4,0)),Piece('black','rook',(7,0)),
                    Piece('black','knight',(6,0)),Piece('black','bishop',(5,0)))
for x in range(8):
    black_pieces.add(Pawn('black',(x,1)))

#Game loop
while True:
    #Event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Draw and update the screen
    screen.blit(board_background, (0,0))

    white_pieces.update(events)
    white_pieces.draw(screen)
    
    black_pieces.update(events)
    black_pieces.draw(screen)

    pygame.display.update()
    clock.tick(60)