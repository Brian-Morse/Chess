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
        self.has_moved_before = has_moved
        self.has_moved = has_moved
        self.dirs = []
        self.range = 1
        self.is_clicked = False

    def set_side(self, side, sides):
        self.side = side
        self.sides = sides
        self.image = pygame.image.load(f'images/{side}_{self.type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = coord_to_pixel(*self.pos))

    def set_pos(self, new_pos):
        """Sets the position of the piece"""
        self.pos = new_pos

    def set_is_clicked(self, new_value):
        """Sets the is clicked attribute of this piece"""
        self.is_clicked = new_value

    def check_side(self):
        return self.side == self.sides[0].get_side()

    def get_type(self):
        return self.type

    def get_has_moved(self):
        """Return the status of if this piece has moved"""
        return self.has_moved

    def set_has_moved(self, new_value):
        """Sets the has moved attribute"""
        self.has_moved = new_value

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
        return (self,self.prev_pos,self.pos,self.has_moved_before)

    def update_rect(self):
        self.rect.topleft = coord_to_pixel(*self.pos)

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
                                self.has_moved_before = self.has_moved
                                self.has_moved = True
                                self.just_moved = True
                                if self.check_side():
                                    collide = pygame.sprite.spritecollide(self, 
                                                                self.sides[1],False)
                                    self.sides[1].remove(collide)
                                    for piece in collide:
                                        Side.dead_pieces.append((piece,Side.move_count))
                                else:
                                    collide = pygame.sprite.spritecollide(self,
                                                                self.sides[0],
                                                                False)
                                    self.sides[0].remove(collide)
                                    for piece in collide:
                                        Side.dead_pieces.append((piece,Side.move_count))
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
            #Check if pawn can lower en passant
            if self.sides[0].can_lower_en_passant(self):
                possible_moves.append((self.pos[0]-1, self.pos[1]-1))
            #Check if pawn can higher en passant
            if self.sides[0].can_higher_en_passant(self):
                possible_moves.append((self.pos[0]+1, self.pos[1]-1))
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
                #Check if pawn can lower en passant
                if self.sides[1].can_lower_en_passant(self):
                    possible_moves.append((self.pos[0]-1, self.pos[1]+1))
                #Check if pawn can higher en passant
                if self.sides[1].can_higher_en_passant(self):
                    possible_moves.append((self.pos[0]+1, self.pos[1]+1))
        return possible_moves

    def update(self, events):
        """Update the pawn action and visual"""
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
                                self.has_moved_before = self.has_moved
                                self.has_moved = True
                                self.just_moved = True
                                if self.check_side():
                                    collide = pygame.sprite.spritecollide(self, 
                                                                self.sides[1], 
                                                                False)
                                    if not collide:
                                        for pawn in [piece for piece in
                                                self.sides[1] if 
                                                piece.get_pos() == 
                                                (self.pos[0],self.pos[1]+1)]:
                                            self.sides[1].remove(pawn)
                                            Side.dead_pieces.append((pawn,Side.move_count))
                                    else:
                                        self.sides[1].remove(collide)
                                        for piece in collide:
                                            Side.dead_pieces.append((piece,Side.move_count))
                                else:
                                    collide = pygame.sprite.spritecollide(self,
                                                                self.sides[0],
                                                                False)
                                    if not collide:
                                        for pawn in [piece for piece in
                                                self.sides[0] if 
                                                piece.get_pos() == 
                                                (self.pos[0],self.pos[1]-1)]:
                                            self.sides[0].remove(pawn)
                                            Side.dead_pieces.append((pawn,Side.move_count))
                                    else:
                                        self.sides[0].remove(collide)
                                        for piece in collide:
                                            Side.dead_pieces.append((piece,Side.move_count))
                    else:
                        #See if the piece is being clicked for the first time
                        if self.pos == event_pos:
                            self.is_clicked = True

        if self.is_clicked:
            #Visual continuance
            screen.blit(avail_move_surf,coord_to_pixel(*self.pos))
            self.show_moves()

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
    
    def get_move_locs(self):
        """Get all the moves for the king"""
        moves = super().get_move_locs()
        if self.check_side():
            if self.sides[0].can_short_castle():
                moves.append((self.pos[0]+2,self.pos[1]))
            if self.sides[0].can_long_castle():
                moves.append((self.pos[0]-2,self.pos[1]))
        else:
            if self.sides[1].can_short_castle():
                moves.append((self.pos[0]+2,self.pos[1]))
            if self.sides[1].can_long_castle():
                moves.append((self.pos[0]-2,self.pos[1]))
        return moves

class Side(pygame.sprite.Group):
    """Group class to hold a player's pieces"""

    #Collection of sides
    sides = []
    move_made = False
    dead_pieces = []
    created_pieces = []
    moves = []
    move_count = 0

    def __init__(self, side, *sprites: Piece):
        """Initializes group variables to track game"""
        #Establish side before adding sprites
        self.side = side
        self.sides.append(self)
        #Now do the normal initialization to add sprites to the group
        super().__init__(*sprites)
        self.last_move = ()
        for piece in self:
            if piece.get_type() == 'king':
                self.king = piece

    def add(self, *sprites: Piece):
        """Adds pieces to the side"""
        super().add(*sprites)
        for sprite in sprites:
            sprite.set_side(self.side,self.sides)

    def can_short_castle(self):
        """Check if short castling is a possible move, true if so"""
        #Get king position
        x,y = self.king.get_pos()
        #Make sure the king is not in check and has not moved
        if not self.king.get_has_moved() and not self.test_if_check():
            #Make sure the spaces next to king is empty
            if (not ([piece for piece in self if piece.get_pos() == (x+1, y)] 
                or [piece for piece in self if piece.get_pos() == (x+2,y)])):
                #Make sure the rook is there and has not moved
                if [piece for piece in self if piece.get_pos() == (x+3, y) and piece.get_type() == 'rook' and not piece.get_has_moved()]:
                    #Make sure one space will not put king in check
                    self.king.set_pos((x+1,y))
                    if not self.test_if_check():
                        #Make sure final space will not put king in check
                        self.king.set_pos((x+2,y))
                        if not self.test_if_check():
                            #Return king to space
                            self.king.set_pos((x,y))
                            return True
        #Return king to space
        self.king.set_pos((x,y))
        return False
    
    def can_long_castle(self):
        """Check if long castling is a possible move, true if so"""
        #Get king position
        x,y = self.king.get_pos()
        #Make sure the king is not in check and has not moved
        if not self.king.get_has_moved() and not self.test_if_check():
            #Make sure the spaces next to king is empty
            if (not ([piece for piece in self if piece.get_pos() == (x-1, y)] 
                or [piece for piece in self if piece.get_pos() == (x-2,y)]
                or [piece for piece in self if piece.get_pos() == (x-3,y)])):
                #Make sure the rook is there and has not moved
                if [piece for piece in self if piece.get_pos() == (x-4, y) and piece.get_type() == 'rook' and not piece.get_has_moved()]:
                    #Make sure one space will not put king in check
                    self.king.set_pos((x-1,y))
                    if not self.test_if_check():
                        #Make sure final space will not put king in check
                        self.king.set_pos((x-2,y))
                        if not self.test_if_check():
                            #Return king to space
                            self.king.set_pos((x,y))
                            return True
        #Return king to space
        self.king.set_pos((x,y))
        return False

    def can_lower_en_passant(self, pawn):
        """Check if pawn can en passant into a lower x position"""
        #Get pawn position
        x,y = pawn.get_pos()
        #Check which side is being dealt with
        if self.check_side():
            #Check if pawn is at right y position and there is a lower position
            if y == 3 and x != 0:
                #Check if a pawn just moved double space
                other_move = self.sides[1].get_last_move()
                if (other_move[0].get_type() == 'pawn' and 
                    other_move[1][1] == 1 and other_move[2] == (x-1, y)):
                    return True
        else:
            #Check if pawn is at right y position and there is a lower position
            if y == 4 and x != 0:
                #Check if a pawn just moved double space
                other_move = self.sides[0].get_last_move()
                if (other_move[0].get_type() == 'pawn' and 
                    other_move[1][1] == 6 and other_move[2] == (x-1, y)):
                    return True
        #Can't lower en passant
        return False
    
    def can_higher_en_passant(self, pawn):
        """Check if pawn can en passant into a higher x position"""
        #Get pawn position
        x,y = pawn.get_pos()
        #Check which side is being dealt with
        if self.check_side():
            #Check if pawn is at right y position and there is a higher position
            if y == 3 and x != 7:
                #Check if a pawn just moved double space
                other_move = self.sides[1].get_last_move()
                if (other_move[0].get_type() == 'pawn' and 
                    other_move[1][1] == 1 and other_move[2] == (x+1, y)):
                    return True
        else:
            #Check if pawn is at right y position and there is a higher position
            if y == 4 and x != 7:
                #Check if a pawn just moved double space
                other_move = self.sides[0].get_last_move()
                if (other_move[0].get_type() == 'pawn' and 
                    other_move[1][1] == 6 and other_move[2] == (x+1, y)):
                    return True
        #Can't higher en passant
        return False

    def get_side(self):
        """Returns the side of this team"""
        return self.side
    
    def get_last_move(self):
        """Returns the last move"""
        return self.last_move

    def set_last_move(self, new_last_move):
        """Sets the last move of this side"""
        self.last_move = new_last_move

    def get_promote_image(self):
        """Gives the image for the promotion of this side"""
        return pygame.image.load(f'images/{self.side}_promotion.png').convert()

    def get_info(self):
        """Retrieve important info from pieces to see what is 
        available"""
        #Track total moves possible
        pos_moves = 0
        #Go through every piece to get info  
        for piece in self:
            pos_moves += len(piece.get_move_locs())
            #Piece just moved, get the move spaces
            if piece.get_just_moved():
                self.last_move = piece.get_move_info()
                Side.moves.append(self.last_move)
                Side.move_count += 1
                Side.move_made = True
                #Check for promotion
                if piece.get_type() == 'pawn' and (piece.get_pos()[1] == 0 or 
                                             piece.get_pos()[1] == 7):
                    if self.check_side():
                        self.sides[0].remove(piece)
                        Side.dead_pieces.append((piece,Side.move_count-1))
                        return FIRST_PROMOTION
                    else:
                        self.sides[1].remove(piece)
                        Side.dead_pieces.append((piece,Side.move_count-1))
                        return SECOND_PROMOTION
                #Check for short castling
                if (piece.get_type() == 'king' and 
                    self.last_move[2][0] - self.last_move[1][0] == 2):
                    if self.check_side():
                        mov_rook = [rook for rook in self 
                                    if rook.get_pos() == (7,7)]
                        mov_rook[0].set_pos((5,7))
                        mov_rook[0].set_has_moved(True)
                    else:
                        mov_rook = [rook for rook in self 
                                    if rook.get_pos() == (7,0)]
                        mov_rook[0].set_pos((5,0))
                        mov_rook[0].set_has_moved(True)
                #Check for long castling
                if (piece.get_type() == 'king' and 
                    self.last_move[2][0] - self.last_move[1][0] == -2):
                    if self.check_side():
                        mov_rook = [rook for rook in self 
                                    if rook.get_pos() == (0,7)]
                        mov_rook[0].set_pos((3,7))
                        mov_rook[0].set_has_moved(True)
                    else:
                        mov_rook = [rook for rook in self 
                                    if rook.get_pos() == (0,0)]
                        mov_rook[0].set_pos((3,0))
                        mov_rook[0].set_has_moved(True)


        #Check for checkmate and stalemate
        if pos_moves == 0:
            if self.test_if_check():
                return CHECKMATE
            else:
                return STALEMATE
        return ACTIVE_GAME

    def draw_check(self):
        """Draws check if in check"""
        if self.test_if_check():
            screen.blit(check_surf,coord_to_pixel(*self.king.get_pos()))

    def draw_last_move(self):
        """Draws the last move of this side"""
        if self.last_move:
            screen.blit(last_move_surf,coord_to_pixel(*self.last_move[1]))
            screen.blit(last_move_surf,coord_to_pixel(*self.last_move[2]))

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

    @staticmethod
    def undo_move():
        """Undoes the last move of the game"""
        if Side.moves:
            #Unclick all of the pieces
            for side in Side.sides:
                for piece in side:
                    piece.set_is_clicked(False)
            #Get the move info that needs to be reversed and new number of moves
            undid_move = Side.moves.pop()
            Side.move_count -= 1
            #Move the piece back to its old spot and set the has moved attribute
            undid_move[0].set_pos(undid_move[1])
            undid_move[0].set_has_moved(undid_move[3])
            #Check if rook needs to be moved back due to short castling
            if (undid_move[0].get_type() == 'king' and 
                undid_move[2][0] - undid_move[1][0] == 2):
                if undid_move[0].check_side():
                    mov_rook = [rook for rook in Side.sides[0] 
                                if rook.get_pos() == (5,7)]
                    mov_rook[0].set_pos((7,7))
                    mov_rook[0].set_has_moved(False)
                else:
                    mov_rook = [rook for rook in Side.sides[1] 
                                if rook.get_pos() == (5,0)]
                    mov_rook[0].set_pos((7,0))
                    mov_rook[0].set_has_moved(False)
            #Check if rook needs to be moved back due to long castling
            if (undid_move[0].get_type() == 'king' and 
                undid_move[2][0] - undid_move[1][0] == -2):
                    if undid_move[0].check_side():
                        mov_rook = [rook for rook in Side.sides[0] 
                                    if rook.get_pos() == (3,7)]
                        mov_rook[0].set_pos((0,7))
                        mov_rook[0].set_has_moved(False)
                    else:
                        mov_rook = [rook for rook in Side.sides[1] 
                                    if rook.get_pos() == (3,0)]
                        mov_rook[0].set_pos((0,0))
                        mov_rook[0].set_has_moved(False)
            #Correct the last move info
            if undid_move[0].check_side():
                if Side.move_count >= 2:
                    Side.sides[0].set_last_move(Side.moves[-2])
                else:
                    Side.sides[0].set_last_move(())
            else:
                if Side.move_count >= 2:
                    Side.sides[1].set_last_move(Side.moves[-2])
                else:
                    Side.sides[1].set_last_move(())
            #Restore any captured pieces
            to_restore = [piece for piece in Side.dead_pieces if piece[1] == Side.move_count]
            for piece in to_restore:
                Side.dead_pieces.remove(piece)
                if piece[0].check_side():
                    Side.sides[0].add(piece[0])
                else:
                    Side.sides[1].add(piece[0])
            #Remove any promoted pieces that are no longer present
            to_remove = [piece for piece in Side.created_pieces if piece[1] == Side.move_count]
            for piece in to_remove:
                Side.created_pieces.remove(piece)
                if piece[0].check_side():
                    Side.sides[0].remove(piece[0])
                else:
                    Side.sides[1].remove(piece[0])
                piece[0].kill()
            #Toggle the move
            toggle_turn()

#Constants
SQUARE_SIZE = 80
HEIGHT = 8
WIDTH = 8
ACTIVE_GAME = 0
FIRST_PROMOTION = 1
SECOND_PROMOTION = -1
CHECKMATE = 2
STALEMATE = 3
FIRST_TURN = 1
SECOND_TURN = 0
FIRST_PERSPECTIVE = FIRST_TURN
SECOND_PERSPECTIVE = SECOND_TURN

def coord_to_pixel(x,y):
    """Returns the pixel location of a provided coordinate"""
    #First display
    if perspective == FIRST_PERSPECTIVE:
        return (x*SQUARE_SIZE,y*SQUARE_SIZE)
    #Second display
    new_x = abs(x-(WIDTH-1))
    new_y = abs(y-(HEIGHT-1))
    return (new_x*SQUARE_SIZE,new_y*SQUARE_SIZE)
    
def pixel_to_coord(x,y):
    """Returns the coordinate location of a provided pixel"""
    #First display
    if perspective == FIRST_PERSPECTIVE:
        return ((int)(x/SQUARE_SIZE),(int)(y/SQUARE_SIZE))
    #Second display
    x = (int)(x/SQUARE_SIZE)
    y = (int)(y/SQUARE_SIZE)
    return (abs(x-(WIDTH-1)),abs(y-(HEIGHT-1)))

def collide_point(group,x,y):
    """Returns a list of all pieces that collide with a coordinate"""
    return [piece for piece in group if piece.get_pos() == (x,y)]

def toggle_turn():
    """Toggles the turn of the game"""
    global turn, perspective
    if turn == FIRST_TURN:
        turn = SECOND_TURN
        if flip_screen:
            perspective = SECOND_PERSPECTIVE
    else:
        turn = FIRST_TURN
        if flip_screen:
            perspective = FIRST_PERSPECTIVE
    for side in Side.sides:
        for piece in side:
            piece.update_rect()

#Screen and clock set up
pygame.init()
screen = pygame.display.set_mode((WIDTH*SQUARE_SIZE,HEIGHT*SQUARE_SIZE))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

#Organization
game_state = ACTIVE_GAME
turn = FIRST_TURN
show_end_screen = True
flip_screen = False
perspective = FIRST_PERSPECTIVE

#Background
board_background = pygame.image.load('images/chess_board.png').convert()

avail_move_surf = pygame.image.load('images/avail_move.png').convert_alpha()

last_move_surf = pygame.image.load('images/last_move.png').convert_alpha()

check_surf = pygame.image.load('images/check.png').convert_alpha()

checkmate_surf = pygame.image.load('images/checkmate_screen.png').convert()

draw_surf = pygame.image.load('images/draw_screen.png').convert()

#White pieces set up
first_pieces = Side('white', Rook((0,7)),Knight((1,7)),
                    Bishop((2,7)),Queen((3,7)),
                    King((4,7)),Rook((7,7)),
                    Knight((6,7)),Bishop((5,7)))
for x in range(8):
    first_pieces.add(Pawn((x,6)))

first_promote_surf = first_pieces.get_promote_image()

#Black pieces set up
second_pieces = Side('black', Rook((0,0)),Knight((1,0)),
                    Bishop((2,0)),Queen((3,0)),
                    King((4,0)),Rook((7,0)),
                    Knight((6,0)),Bishop((5,0)))
for x in range(8):
    second_pieces.add(Pawn((x,1)))

second_promote_surf = second_pieces.get_promote_image()

#Game loop
while True:
    #Event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == ACTIVE_GAME:
            if event.type == pygame.KEYUP:
                #Reset game
                if event.key == pygame.K_r:
                    #Reset game state trackers
                    game_state = ACTIVE_GAME
                    turn = FIRST_TURN
                    show_end_screen = True
                    #Reset sides and pieces
                    Side.sides = []
                    Side.move_made = False
                    Side.moves = []
                    Side.move_count = 0
                    Side.dead_pieces = []
                    Side.created_pieces = []

                    #White pieces set up
                    first_pieces = Side('white', Rook((0,7)),Knight((1,7)),
                                        Bishop((2,7)),Queen((3,7)),
                                        King((4,7)),Rook((7,7)),
                                        Knight((6,7)),Bishop((5,7)))
                    for x in range(8):
                        first_pieces.add(Pawn((x,6)))
                    #Black pieces set up
                    second_pieces = Side('black', Rook((0,0)),Knight((1,0)),
                                        Bishop((2,0)),Queen((3,0)),
                                        King((4,0)),Rook((7,0)),
                                        Knight((6,0)),Bishop((5,0)))
                    for x in range(8):
                        second_pieces.add(Pawn((x,1)))
                #Undo move
                elif event.key == pygame.K_u:
                    Side.undo_move()
                #Lock or release screen flipping
                elif event.key == pygame.K_f:
                    flip_screen = not flip_screen
                    if flip_screen:
                        if turn == FIRST_TURN:
                            perspective = FIRST_PERSPECTIVE
                        else:
                            perspective = SECOND_PERSPECTIVE
                        for side in Side.sides:
                            for piece in side:
                                piece.update_rect()
        elif game_state == FIRST_PROMOTION:
            if event.type == pygame.MOUSEBUTTONUP:
                coord = pixel_to_coord(*event.pos)
                if perspective == FIRST_PERSPECTIVE:
                    promote_coord = first_pieces.get_last_move()[2]
                    if coord[0] == promote_coord[0]:
                        if coord[1] == promote_coord[1]:
                            piece = Queen(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                            event.pos = (-1,-1)
                        if coord[1] == promote_coord[1]+1:
                            piece = Bishop(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]+2:
                            piece = Knight(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]+3:
                            piece = Rook(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                else:
                    promote_coord = first_pieces.get_last_move()[2]
                    if coord[0] == promote_coord[0]:
                        if coord[1] == promote_coord[1]+3:
                            piece = Queen(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]+2:
                            piece = Bishop(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]+1:
                            piece = Knight(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]:
                            piece = Rook(promote_coord,has_moved=True)
                            first_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                            event.pos = (-1,-1)
        elif game_state == SECOND_PROMOTION:
            if event.type == pygame.MOUSEBUTTONUP:
                coord = pixel_to_coord(*event.pos)
                if perspective == SECOND_PERSPECTIVE:
                    promote_coord = second_pieces.get_last_move()[2]
                    if coord[0] == promote_coord[0]:
                        if coord[1] == promote_coord[1]:
                            piece = Queen(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                            event.pos = (-1,-1)
                        if coord[1] == promote_coord[1]-1:
                            piece = Bishop(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]-2:
                            piece = Knight(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]-3:
                            piece = Rook(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                else:
                    promote_coord = second_pieces.get_last_move()[2]
                    if coord[0] == promote_coord[0]:
                        if coord[1] == promote_coord[1]-3:
                            piece = Queen(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]-2:
                            piece = Bishop(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]-1:
                            piece = Knight(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                        if coord[1] == promote_coord[1]:
                            piece = Rook(promote_coord,has_moved=True)
                            second_pieces.add(piece)
                            Side.created_pieces.append((piece,Side.move_count-1))
                            game_state = ACTIVE_GAME
                            event.pos = (-1,-1)
        elif game_state == CHECKMATE or game_state == STALEMATE:
            if event.type == pygame.KEYUP:
                #Toggle showing end screen
                if event.key == pygame.K_b:
                    show_end_screen = not show_end_screen
                #Reset game
                elif event.key == pygame.K_SPACE:
                    #Reset game state trackers
                    game_state = ACTIVE_GAME
                    turn = FIRST_TURN
                    show_end_screen = True
                    #Reset sides and pieces
                    Side.sides = []
                    Side.move_made = False
                    Side.moves = []
                    Side.move_count = 0
                    Side.dead_pieces = []
                    Side.created_pieces = []
                    #White pieces set up
                    first_pieces = Side('white', Rook((0,7)),Knight((1,7)),
                                        Bishop((2,7)),Queen((3,7)),
                                        King((4,7)),Rook((7,7)),
                                        Knight((6,7)),Bishop((5,7)))
                    for x in range(8):
                        first_pieces.add(Pawn((x,6)))
                    #Black pieces set up
                    second_pieces = Side('black', Rook((0,0)),Knight((1,0)),
                                        Bishop((2,0)),Queen((3,0)),
                                        King((4,0)),Rook((7,0)),
                                        Knight((6,0)),Bishop((5,0)))
                    for x in range(8):
                        second_pieces.add(Pawn((x,1)))


    if game_state == ACTIVE_GAME:
        #Draw background
        screen.blit(board_background, (0,0))
        #Update pieces
        if turn == FIRST_TURN:
            first_pieces.update(events)
            game_state = first_pieces.get_info()
            first_pieces.draw_check()
            second_pieces.draw_last_move()
        else:
            second_pieces.update(events)
            game_state = second_pieces.get_info()
            second_pieces.draw_check()
            first_pieces.draw_last_move()
        #Draw pieces
        first_pieces.draw(screen)
        second_pieces.draw(screen)
    elif game_state == FIRST_PROMOTION:
        if perspective == FIRST_PERSPECTIVE:
            screen.blit(first_promote_surf,coord_to_pixel(*first_pieces.get_last_move()[2]))
        else:
            screen.blit(first_promote_surf,coord_to_pixel(first_pieces.get_last_move()[2][0],first_pieces.get_last_move()[2][1]+3))
    elif game_state == SECOND_PROMOTION:
        if perspective == SECOND_PERSPECTIVE:
            screen.blit(second_promote_surf,coord_to_pixel(*second_pieces.get_last_move()[2]))
        else:
            screen.blit(second_promote_surf,coord_to_pixel(second_pieces.get_last_move()[2][0],second_pieces.get_last_move()[2][1]-3))
    elif game_state == CHECKMATE:
        screen.blit(board_background, (0,0))
        if show_end_screen:
            screen.blit(checkmate_surf, (160,160))
        else:
            first_pieces.draw(screen)
            second_pieces.draw(screen)
    elif game_state == STALEMATE:
        screen.blit(board_background, (0,0))
        if show_end_screen:
            screen.blit(draw_surf,(160,160))
        else:
            first_pieces.draw(screen)
            second_pieces.draw(screen)

    #Check to alter turn
    if Side.move_made and game_state == ACTIVE_GAME:
        toggle_turn()
        Side.move_made = False

    pygame.display.update()
    clock.tick(60)