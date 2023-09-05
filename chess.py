import pygame
import sys

class Piece(pygame.sprite.Sprite):
    """Sprite class to represent all possible chess pieces"""
    def __init__(self, type, pos, has_moved = False):
        """Initiates the general chess piece"""
        super().__init__()
        self.type = type
        self.pos = pos
        self.prev_pos = (0,0)
        self.just_moved = False
        self.has_moved = has_moved
        self.dirs = []
        self.range = 1
        self.is_clicked = False

    def set_side(self, side, sides):
        self.side = side
        self.sides = sides
        self.image = pygame.image.load(f'images/{side}_{self.type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = coord_to_pixel(*self.pos))

    def check_side(self):
        return self.side == self.sides[0].get_side()

    def get_type(self):
        return self.type

    def get_pos(self):
        return self.pos

    def get_pressure(self):
        """Returns the positions that this chess piece puts pressure on"""
        pressure = []
        if self.check_side():
            for dir in self.dirs:
                dir_range = self.range
                x = self.pos[0] + dir[0]
                y = self.pos[1] + dir[1]
                while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                       y < HEIGHT):
                    pressure.append((x,y))
                    dir_range -= 1
                    if (collide_point(self.sides[1],x,y) or 
                        collide_point(self.sides[0],x,y)):
                        dir_range = 0
                    x += dir[0]
                    y += dir[1]
                # while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                #        y < HEIGHT and not collide_point(self.sides[0],x,y)):
                #     pressure.append((x,y))
                #     dir_range -= 1
                #     if (collide_point(self.sides[1],x,y)
                #         ):
                #         dir_range = 0
                #     x += dir[0]
                #     y += dir[1]
        else:
            for dir in self.dirs:
                dir_range = self.range
                x = self.pos[0] + dir[0]
                y = self.pos[1] + dir[1]
                while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                       y < HEIGHT):
                    pressure.append((x,y))
                    dir_range -= 1
                    if (collide_point(self.sides[0],x,y) or 
                        collide_point(self.sides[1],x,y)):
                        dir_range = 0
                    x += dir[0]
                    y += dir[1]
                # while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                #        y < HEIGHT and not collide_point(self.sides[1],x,y)):
                #     pressure.append((x,y))
                #     dir_range -= 1
                #     if (collide_point(self.sides[0],x,y)
                #         ):
                #         dir_range = 0
                #     x += dir[0]
                #     y += dir[1]
        return pressure

    def get_possible_move_locs(self):
        """Returns the possible move locations, ignoring check"""
        possible_moves = []
        if self.check_side():
            for dir in self.dirs:
                dir_range = self.range
                x = self.pos[0] + dir[0]
                y = self.pos[1] + dir[1]
                while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                       y < HEIGHT and not collide_point(self.sides[0],x,y)):
                    possible_moves.append((x,y))
                    dir_range -= 1
                    if collide_point(self.sides[1],x,y):
                        dir_range = 0
                    x += dir[0]
                    y += dir[1]
        else:
            for dir in self.dirs:
                dir_range = self.range
                x = self.pos[0] + dir[0]
                y = self.pos[1] + dir[1]
                while (dir_range != 0 and x >= 0 and x < WIDTH and y >= 0 and 
                       y < HEIGHT and not collide_point(self.sides[1],x,y)):
                    possible_moves.append((x,y))
                    dir_range -= 1
                    if collide_point(self.sides[0],x,y):
                        dir_range = 0
                    x += dir[0]
                    y += dir[1]
        return possible_moves

    def get_move_locs(self):
        """Returns locations this piece can move to"""
        moves = []
        #Go through all the moves typically afforded to the piece
        for move in self.get_possible_move_locs():
            #Save old position and test new position if check results
            old_pos = self.pos
            self.pos = move
            if self.check_side():
                causes_check = self.sides[0].test_if_check(move = move)
            else:
                causes_check = self.sides[1].test_if_check(move = move)
            #Can move to this space
            if not causes_check:
                moves.append(move)
            #Return to old position
            self.pos = old_pos
        return moves

    def show_moves(self):
        """Visualize the locations the chess piece can move to"""
        moves = self.get_move_locs()
        for move in moves:
            screen.blit(avail_move_surf,coord_to_pixel(*move))

    def get_just_moved(self):
        """Check if this piece had just moved"""
        return self.just_moved
    
    def get_move_info(self):
        """Get the info for the move this piece just made"""
        self.just_moved = False
        return (self.type,self.prev_pos,self.pos)

    def update(self, events):
        """Update the chess piece action and visual"""
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    event_pos = pixel_to_coord(*event.pos)
                    #This piece is already clicked
                    if self.is_clicked:
                        #Clicking the same piece
                        if self.pos == event_pos:
                            self.is_clicked = True
                        #Check for other possibilities and take action
                        else:
                            self.is_clicked = False
                            if event_pos in self.get_move_locs():
                                self.prev_pos = self.pos
                                self.pos = event_pos
                                self.rect.topleft = coord_to_pixel(*self.pos)
                                self.has_moved = True
                                self.just_moved = True
                                if self.check_side():
                                    pygame.sprite.spritecollide(self, 
                                                                self.sides[1], 
                                                                dokill = True)
                                else:
                                    pygame.sprite.spritecollide(self,
                                                                self.sides[0],
                                                                dokill=True)
                    else:
                        #See if the piece is being clicked for the first time
                        if self.pos == event_pos:
                            self.is_clicked = True

        if self.is_clicked:
            #Visual continuance
            screen.blit(avail_move_surf,coord_to_pixel(*self.pos))
            self.show_moves()

class Pawn(Piece):
    """A Pawn chess piece, most common piece from chess"""
    def __init__(self, pos, has_moved = False):
        """Initiates the Pawn piece"""
        super().__init__('pawn', pos, has_moved)

    def get_pressure(self):
        """Returns the diagonal points of applied pressure"""
        x,y = self.pos
        if self.check_side():
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
        if self.check_side():
            #Check if there are diagonal points to capture
            for move in pressure:
                if collide_point(self.sides[1],*move):
                    possible_moves.append(move)
            #Checks if there is a piece ahead of the pawn
            if (not collide_point(self.sides[1], self.pos[0], self.pos[1]-1) 
                and not collide_point(self.sides[0], self.pos[0],
                                      self.pos[1]-1)):
                
                possible_moves.append((self.pos[0],self.pos[1]-1))
                #Checks if the pawn has moved and if there is a piece two 
                #spaces ahead
                if (not self.has_moved and not 
                    collide_point(self.sides[1], self.pos[0], self.pos[1]-2) 
                    and not collide_point(self.sides[0], self.pos[0],
                                          self.pos[1]-2)):
                    
                    possible_moves.append((self.pos[0],self.pos[1]-2))
        else:
            #Checks if there are diagonal points to capture
            for move in pressure:
                if collide_point(self.sides[0],*move):
                    possible_moves.append(move)
            #Checks if there is a piece ahead of the pawn
            if (not collide_point(self.sides[1], self.pos[0], self.pos[1]+1) 
                and not collide_point(self.sides[0], self.pos[0],
                                      self.pos[1]+1)):
                
                possible_moves.append((self.pos[0],self.pos[1]+1))
                #Checks if the pawn has moved and if there is a piece two 
                #spaces ahead
                if (not self.has_moved and not 
                    collide_point(self.sides[1], self.pos[0], self.pos[1]+2) 
                    and not collide_point(self.sides[0], self.pos[0],
                                          self.pos[1]+2)):
                    possible_moves.append((self.pos[0],self.pos[1]+2))
        return possible_moves

class Knight(Piece):
    """A knight chess piece, moves in Ls"""
    def __init__(self, pos, has_moved = False):
        """Initializes the knight piece"""
        super().__init__('knight',pos,has_moved)
        #Set up the knight moves
        self.dirs = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

class Bishop(Piece):
    """A bishop chess piece, moves in diagonals"""
    def __init__(self, pos, has_moved = False):
        """Initializes the bishop piece"""
        super().__init__('bishop',pos,has_moved)
        #Set up the bishop moves
        self.dirs = [(1,1),(-1,-1),(1,-1),(-1,1)]
        self.range = -1

class Rook(Piece):
    """A rook chess piece, moves in horizontals"""
    def __init__(self, pos, has_moved = False):
        """Initializes the rook piece"""
        super().__init__('rook',pos,has_moved)
        #Set up the rook moves
        self.dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        self.range = -1

class Queen(Piece):
    """A queen chess piece, moves in all directions, most powerful piece"""
    def __init__(self, pos, has_moved = False):
        """Initializes the queen piece"""
        super().__init__('queen',pos,has_moved)
        #Set up the queen moves
        self.dirs = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
        self.range = -1

class King(Piece):
    """A king chess piece, the most important of all pieces"""
    def __init__(self, pos, has_moved = False):
        """Initializes the king piece"""
        super().__init__('king',pos,has_moved)
        #Set up the king moves
        self.dirs = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]

class Side(pygame.sprite.Group):
    """Group class to hold a player's pieces"""

    #Collection of sides
    sides = []

    def __init__(self, side, *sprites: Piece):
        """Initializes group variables to track game"""
        #Establish side before adding sprites
        self.side = side
        self.sides.append(self)
        #Now do the normal initialization to add sprites to the group
        super().__init__(*sprites)
        self.enpassant = []
        self.last_move = ()
        for piece in self:
            if piece.get_type() == 'king':
                self.king = piece

    def add(self, *sprites: Piece):
        super().add(*sprites)
        for sprite in sprites:
            sprite.set_side(self.side,self.sides)
    
    def get_side(self):
        return self.side

    def get_info(self):
        """Retrieve important info from pieces to see what is 
        available"""  
        for piece in self:
            if piece.get_just_moved():
                self.last_move = piece.get_move_info()

    def group_draw(self):
        """Draws important info for the side"""
        #Draws the latest move
        if self.last_move:
            screen.blit(last_move_surf,coord_to_pixel(*self.last_move[1]))
            screen.blit(last_move_surf,coord_to_pixel(*self.last_move[2]))
        if self.test_if_check():
            screen.blit(check_surf,coord_to_pixel(*self.king.get_pos()))

    def check_side(self):
        return self.side == self.sides[0].get_side()

    def test_if_check(self, move = None):
        """Returns true if this side is in check, false otherwise"""
        #Finds if any black piece pressures the white king
        if self.check_side():
            for piece in self.sides[1]:
                #Piece is hypothetically captured
                if piece.get_pos() == move:
                    continue
                #Check if this piece is putting the king in check
                if self.king.get_pos() in piece.get_pressure():
                    return True
        #Finds if any white piece pressures the black king
        else:
            for piece in self.sides[0]:
                #Piece is hypothetically captured
                if piece.get_pos() == move:
                    continue
                if self.king.get_pos() in piece.get_pressure():
                    return True
        return False


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
    return [piece for piece in group if piece.get_pos() == (x,y)]

#Screen and clock set up
pygame.init()
screen = pygame.display.set_mode((WIDTH*SQUARE_SIZE,HEIGHT*SQUARE_SIZE))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

#Background
board_background = pygame.image.load('images/chess_board.png').convert()

avail_move_surf = pygame.image.load('images/avail_move.png').convert_alpha()

last_move_surf = pygame.image.load('images/last_move.png').convert_alpha()

check_surf = pygame.image.load('images/check.png').convert_alpha()

#White pieces set up
white_pieces = Side('white', Rook((0,7)),Knight((1,7)),
                    Bishop((2,7)),Queen((3,7)),
                    King((4,7)),Rook((7,7)),
                    Knight((6,7)),Bishop((5,7)))
for x in range(8):
    white_pieces.add(Pawn((x,6)))

#Black pieces set up
black_pieces = Side('black', Rook((0,0)),Knight((1,0)),
                    Bishop((2,0)),Queen((3,0)),
                    King((4,0)),Rook((7,0)),
                    Knight((6,0)),Bishop((5,0)))
for x in range(8):
    black_pieces.add(Pawn((x,1)))


# white_pieces.add(Pawn('white',(4,2)))
# white_pieces.add(Pawn('white',(4,3)))

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
    white_pieces.get_info()
    white_pieces.group_draw()
    white_pieces.draw(screen)
    
    black_pieces.update(events)
    black_pieces.get_info()
    black_pieces.group_draw()
    black_pieces.draw(screen)

    pygame.display.update()
    clock.tick(60)