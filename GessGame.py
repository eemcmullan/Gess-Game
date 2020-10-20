class GessGame:
    """Represents a game of Gess. It will communicate with the Board class to make a move and get the game state,
     and the Player class to get the player's turn, as well as the resign game method"""

    def __init__(self):
        """Initializes the players and board"""
        self._board = Board()
        self._board.make_board()
        self._player_turn = "B"
        self._not_player_turn = "W"

    def get_player_turn(self):
        """Get the current player turn"""
        return self._player_turn

    def set_player_turn(self, player_turn):
        """Sets the current player's turn"""
        self._player_turn = player_turn

    def get_game_state(self, footprint):
        """Returns Black_won, White_won, or Unfinished"""
        ring_pieces = footprint.get_footprint_coords()
        if self.get_player_turn == "B":
            if ring_pieces.values() != "B":
                return "WHITE_WON"
        if self.get_player_turn == "W":
            if ring_pieces.values != "W":
                return "BLACK_WON"
        else:
            return "UNFINISHED"

    def resign_game(self):
        """Allows current player to resign, causing other player to win, updating game state to winner"""
        if self.get_player_turn == "W":
            return self.get_game_state == "BLACK_WON"
        else:
            return self.get_game_state == "WHITE_WON"

    def move_allowed(self, destination, footprint, center):
        """Used to scan the board to check if the trying move is allowed. If it is White's turn, and a 3x3 piece
        that is trying to be moved has a black piece, the move is not legal. Will then return False"""
        
        # if x and y are within board
        if center.get_x() < 17 and center.get_x() < 1:
            return False
        if center.get_y() < 17 and center.get_y() < 1:
            return False
        if destination.get_x() < 17 and destination.get_x() < 1:
            return False
        if destination.get_y() < 17 and destination.get_y() < 1:
            return False
        if footprint.validate_player_pieces(self._not_player_turn) is False:
            return False
        
        # check center piece
        if_center = footprint.get_center_piece() == self._player_turn
        # check direction
        direction = self.get_direction(center, destination)
        if direction == " ":
            return False
        ring_pieces = footprint.get_footprint_coords()
        # can move in direction
        if ring_pieces.get(direction) == "_":
            return False
        length = self.get_distance_length(center, destination, direction)
        if if_center == "_" and length > 3:
            return False
        # check for obstruction
        if self.is_obstructed(direction, center, length, footprint) is False:
            return False
        return True

    def make_move(self, center, destination):
        """Takes game piece's current center, the center's destination, and call the convert method to convert the
        string input to an index on the board. It will use the move_allowed method to determine if the move is legal.
        If not, or if game is already won, will return False. Otherwise will make the move, remove any captured stones,
        update the game state if necessary, update whose turn it is, and return True."""
        
        converted_index = self._board.convert_to_index(center)
        converted_destination = self._board.convert_to_index(destination)
        footprint = self._board.generate_footprint(converted_index)
        
        self.move_allowed(converted_destination, footprint, converted_index)
        if self.get_game_state(footprint) == "BLACK_WON" or self.get_game_state(footprint) == "WHITE_WON":
            return False
        self._board.make_move(center, destination)
        if self.get_player_turn == "W":
            self.set_player_turn("B")
        else:
            self.set_player_turn("W")
        return True

    def move_north(self, center, destination):
        """Determines if footprint can move north"""
        if center.get_x() == destination.get_x():
            if destination.get_y() > center.get_y():
                return True
        else:
            return False

    def move_south(self, center, destination):
        """Determines if footprint can move south"""
        if center.get_x() == destination.get_x():
            if destination.get_y() < center.get_y():
                return True
        else:
            return False

    def move_west(self, center, destination):
        """Determines if footprint can move west"""
        if center.get_y() == destination.get_y():
            if destination.get_x() < center.get_x():
                return True
        else:
            return False

    def move_east(self, center, destination):
        """Determines if footprint can move east"""
        if center.get_y() == destination.get_y():
            if destination.get_x() > center.get_x():
                return True
        else:
            return False

    def move_NE(self, center, destination):
        """Determines if footprint can move NE"""
        x_change = destination.get_x() - center.get_x()
        y_change = destination.get_y() - center.get_y()
        if x_change == y_change and x_change > 0:
            return True
        else:
            return False

    def move_NW(self, center, destination):
        """Determines if footprint can move NW"""
        x_change = destination.get_x() - center.get_x()
        y_change = destination.get_y() - center.get_y()
        if x_change + y_change == 0:
            if x_change < 0:
                return True
        else:
            return False

    def move_SE(self, center, destination):
        """Determines if footprint can move SE"""
        x_change = destination.get_x() - center.get_x()
        y_change = destination.get_y() - center.get_y()
        if x_change + y_change == 0:
            if x_change > 0:
                return True
        else:
            return False

    def move_SW(self, center, destination):
        """Determines if footprint can move SW"""
        x_change = destination.get_x() - center.get_x()
        y_change = destination.get_y() - center.get_y()
        if x_change == y_change and x_change < 0:
            return True
        else:
            return False

    def get_direction(self, center, destination):
        """Uses methods defined above to determine direction of piece"""
        direction = " "
        if self.move_north(center, destination):
            direction = "north"
            return direction
        if self.move_south(center, destination):
            direction = "south"
            return direction
        if self.move_east(center, destination):
            direction = "east"
            return direction
        if self.move_west(center, destination):
            direction = "west"
            return direction
        if self.move_NE(center, destination):
            direction = "NE"
            return direction
        if self.move_NW(center, destination):
            direction = "NW"
            return direction
        if self.move_SE(center, destination):
            direction = "SE"
            return direction
        if self.move_SW(center, destination):
            direction = "SW"
            return direction
        return direction

    def calculate_north(self, center, destination):
        """Calculates difference between y index spaces to move to determine if move is allowed"""
        y_change = destination.get_y() - center.get_y()
        return y_change

    def calculate_south(self, center, destination):
        """Calculates difference between y index spaces to move to determine if move is allowed.
        Multiply by -1 to get positive number"""
        y_change = destination.get_y() - center.get_y()
        return y_change * -1

    def calculate_west(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed.
        Multiply by -1 to get positive number"""
        x_change = destination.get_x() - center.get_x()
        return x_change * -1

    def calculate_east(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed"""
        x_change = destination.get_x() - center.get_x()
        return x_change

    def calculate_NE(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed"""
        x_change = destination.get_x() - center.get_x()
        return x_change

    def calculate_NW(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed.
        Multiply by -1 to get positive number"""
        x_change = destination.get_x() - center.get_x()
        return x_change * -1

    def calculate_SE(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed"""
        x_change = destination.get_x() - center.get_x()
        return x_change

    def calculate_SW(self, center, destination):
        """Calculates difference between x index spaces to move to determine if move is allowed.
        Multiply by -1 to get positive number"""
        x_change = destination.get_x() - center.get_x()
        return x_change * -1

    def get_distance_length(self, center, destination, direction):
        """Defines length a piece can move determined by previous methods"""
        if direction == "north":
            return self.calculate_north(center, destination)
        if direction == "south":
            return self.calculate_south(center, destination)
        if direction == "east":
            return self.calculate_east(center, destination)
        if direction == "west":
            return self.calculate_west(center, destination)
        if direction == "NE":
            return self.calculate_NE(center, destination)
        if direction == "NW":
            return self.calculate_NW(center, destination)
        if direction == "SE":
            return self.calculate_SE(center, destination)
        if direction == "SW":
            return self.calculate_SW(center, destination)

    def is_obstructed(self, direction, center, length, footprint):
        """Used to stop a piece when it moves into same space as another piece"""
        if direction == "north":
            return self.obstructed_north(direction, center, length, footprint)
        if direction == "south":
            return self.obstructed_south(direction, length, footprint)
        if direction == "east":
            return self.obstructed_east(direction, length, footprint)
        if direction == "west":
            return direction
        if direction == "NE":
            return self.obstructed_NE(direction, length, footprint)
        if direction == "NW":
            return self.obstructed_NW(direction, length, footprint)
        if direction == "SE":
            return self.obstructed_SE(direction, length, footprint)
        if direction == "SW":
            return self.obstructed_SW(direction, length, footprint)

    def obstructed_north(self, direction, center, length, footprint):
        """Determines if footprint can move to spot on board based on northern pieces"""
        north_pieces = []
        ring_pieces = footprint.get_footprint_coords()
        if ring_pieces.get("north") != "_":
            north_pieces.append(footprint.generate_piece_coord(direction, center))
        if ring_pieces.get("NE") != "_":
            north_pieces.append(footprint.generate_piece_coord("NE", center))
        if ring_pieces.get("NW") != "_":
            north_pieces.append(footprint.generate_piece_coord("NW", center))
        for i in length - 1:
            for pieces in north_pieces:
                index = Index(pieces.get_x(), pieces.get_y() + i)
                if self._board.get_board_piece(index) != "_":
                    return False
        return True

    def obstructed_south(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on southern pieces"""
        south_pieces = []
        ring_pieces = footprint.get_footprint_coords()
        if ring_pieces.get("south") != "_":
            south_pieces.append(footprint.generate_piece_coord(direction))
        if ring_pieces.get("SE") != "_":
            south_pieces.append(footprint.generate_piece_coord("SE"))
        if ring_pieces.get("SW") != "_":
            south_pieces.append(footprint.generate_piece_coord("SW"))
        for i in length - 1:
            for pieces in south_pieces:
                index = Index(pieces.get_x(), pieces.get_y() - i)
                if self._board.get_board_piece(index) != "_":
                    return False
        return True

    def obstructed_west(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on western pieces"""
        west_pieces = []
        ring_pieces = footprint.get_footprint_coords()
        if ring_pieces.get("west") != "_":
            west_pieces.append(footprint.generate_piece_coord(direction))
        if ring_pieces.get("SW") != "_":
            west_pieces.append(footprint.generate_piece_coord("SW"))
        if ring_pieces.get("NW") != "_":
            west_pieces.append(footprint.generate_piece_coord("NW"))
        for i in length - 1:
            for pieces in west_pieces:
                index = Index(pieces.get_x() - i, pieces.get_y())
                if self._board.get_board_piece(index) != "_":
                    return False
        return True

    def obstructed_east(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on eastern pieces"""
        east_pieces = []
        ring_pieces = footprint.get_footprint_coords()
        if ring_pieces.get("east") != "_":
            east_pieces.append(footprint.generate_piece_coord(direction))
        if ring_pieces.get("SE") != "_":
            east_pieces.append(footprint.generate_piece_coord("SE"))
        if ring_pieces.get("NE") != "_":
            east_pieces.append(footprint.generate_piece_coord("NE"))
        for i in length - 1:
            for pieces in east_pieces:
                index = Index(pieces.get_x() + i, pieces.get_y())
                if self._board.get_board_piece(index) != "_":
                    return False
        return True

    def obstructed_NW(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on NW pieces"""
        is_north = self.obstructed_north(direction, length, footprint)
        is_west = self.obstructed_west(direction, length, footprint)
        if is_north is False:
            return False
        if is_west is False:
            return False
        return True

    def obstructed_NE(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on NE pieces"""
        is_north = self.obstructed_north(direction, length, footprint)
        is_east = self.obstructed_east(direction, length, footprint)
        if is_north is False:
            return False
        if is_east is False:
            return False
        return True

    def obstructed_SE(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on SE pieces"""
        is_south = self.obstructed_south(direction, length, footprint)
        is_east = self.obstructed_east(direction, length, footprint)
        if is_south is False:
            return False
        if is_east is False:
            return False
        return True

    def obstructed_SW(self, direction, length, footprint):
        """Determines if footprint can move to spot on board based on SW pieces"""
        is_south = self.obstructed_south(direction, length, footprint)
        is_west = self.obstructed_west(direction, length, footprint)
        if is_south is False:
            return False
        if is_west is False:
            return False
        return True


class Board:
    """Represents the game board. Will set up and display the board, keep track of the ring locations, convert string
    inputs to its related indexes to allow move to be made, update the new state of the board, and determine
    whether or not current move is allowed by scanning the state of the board. Will communicate with the
    Footprint class to get the footprint information, the Index class to get x and y coordinates, and the
    GessGame class to help the make move method."""

    def __init__(self):
        """Initializes the game board, rings, and a converter from string to index positions"""
        self._game_board = None
        self._ring_location = None
        self._converter = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10,
                           "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19}

    def make_board(self):
        """Makes size of board, rows, columns"""
        self._game_board = \
            [["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],
             ["_", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "_"],
             ["_", "B", "B", "B", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "W", "W", "W", "_"],
             ["_", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "_"],
             ["_", "B", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "W", "_"],
             ["_", "_", "B", "_", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "_", "W", "_", "_"],
             ["_", "B", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "W", "_"],
             ["_", "B", "B", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "W", "W", "_"],
             ["_", "B", "B", "B", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "W", "W", "W", "_"],
             ["_", "B", "B", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "W", "W", "_"],
             ["_", "B", "B", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "W", "W", "_"],
             ["_", "B", "_", "B", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "W", "_", "W", "_"],
             ["_", "B", "B", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "W", "W", "_"],
             ["_", "B", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "W", "_"],
             ["_", "_", "B", "_", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "_", "W", "_", "_"],
             ["_", "B", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "W", "_"],
             ["_", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "_"],
             ["_", "B", "B", "B", "_", "_", "B", "_", "_", "_", "_", "_", "_", "W", "_", "_", "W", "W", "W", "_"],
             ["_", "_", "B", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "W", "_", "_"],
             ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_"]]

    def print_board(self):
        """Prints the board with current footprints"""
        for i in self._game_board:
            print(i)

    def convert_to_index(self, center):
        """Converts a string input to it's related index on the board. Subtract 1 as game-board is 0-indexed. This
        method communicates with the Index class to get x and y coordinates"""
        first_index = center[0]
        first_index = self._converter.get(first_index)
        second_index = int(center[1]) - 1
        return Index(first_index, second_index)

    def generate_footprint(self, converted_index):
        return FootPrint(converted_index, self._game_board)

    def ring_location(self):
        """Determines the location of black and white rings on the board. Will be used before a footprint move. If
        a black or white ring is destroyed, it will determine the winner of the game"""
        # if footprint_ring.values()== "W":
        #   return get_ring_coord
        # if footprint_ring.values == "B":
        #   return get_ring_coord

    def get_board_piece(self, index):
        """Get method to get coordinates of a footprint through it's index"""
        piece = self._game_board[index.get_x()][index.get_y()]
        return piece

    def set_board_piece(self, piece, index):
        """Sets the footprint that just made a move to its new coordinates"""
        self._game_board[index.get_x()][index.get_y()] = piece

    def make_move(self, center, destination):
        """Takes game piece's current center, the center's destination, and call the convert method to convert the
        string input to an index on the board. It will use the move_allowed method to determine if the move is legal.
        If not, or if game is already won, will return False. Otherwise will make the move, remove any captured stones,
        update the game state if necessary, update whose turn it is, and return True."""
        
        converted_index = self.convert_to_index(center)
        converted_destination = self.convert_to_index(destination)
        footprint = FootPrint(converted_index, self._game_board)
        self.update_board(converted_destination, footprint)
        return True

    def update_board(self, destination, footprint):
        """Gets the center piece of the footprint, sets it to the new coordinates it moved, and changes new empty
        spaces to blanks or player's piece"""
        
        center_piece = self.get_board_piece(footprint.get_center())
        # delete 3x3 Block
        old_footprint = footprint.generate_all_piece_coords()
        for i in old_footprint:
            self.set_board_piece("_", i)
            
        # re-insert piece
        self.set_board_piece(center_piece, destination)
        ring_piece = footprint.get_footprint_coords()
        
        # move to after deleting initial spots
        for direction, piece in ring_piece.items():
            new_destination = footprint.generate_destination(direction, destination)
            piece_at_location = self.get_board_piece(new_destination)
            if piece_at_location == "_":
                self.set_board_piece(piece, new_destination)
            else:
                if piece != "_":
                    self.set_board_piece(piece, new_destination)
            # self.set_board_piece("X", new_destination)


class FootPrint:
    """Represents a game piece on the board. It will use the location of where each piece is to determine what moves
    are allowed. Will communicate with the Board class to get piece coordinates"""

    def __init__(self, center, game_board):
        """Initializes the center position of a footprint"""
        self._center = center
        self._center_piece = game_board[center.get_x()][center.get_y()]
        self._footprint_ring = self._footprint_pieces(center, game_board)
        self._direction_dict = {"north": [0, 1], "south": [0, -1], "east": [1, 0], "west": [-1, 0], "NW": [1, -1],
                                "NE": [1, 1], "SW": [-1, -1], "SE": [-1, 1]}

    def get_center(self):
        """Gets the footprint's center coordinates"""
        return self._center

    def get_center_piece(self):
        return self._center_piece

    def _footprint_pieces(self, index, game_board):
        """Determines position of pieces in footprint by finding them by index. Communicates with the Index class
        in order to get the x and y coordinates"""
        north = game_board[index.get_x()][index.get_y() + 1]
        south = game_board[index.get_x()][index.get_y() - 1]
        east = game_board[index.get_x() + 1][index.get_y()]
        west = game_board[index.get_x() - 1][index.get_y()]
        NW = game_board[index.get_x() + 1][index.get_y() - 1]
        NE = game_board[index.get_x() + 1][index.get_y() + 1]
        SW = game_board[index.get_x() - 1][index.get_y() - 1]
        SE = game_board[index.get_x() - 1][index.get_y() + 1]
        footprint_r = {"north": north, "south": south, "east": east, "west": west, "NW": NW, "NE": NE,
                          "SW": SW, "SE": SE}
        return footprint_r

    def generate_piece_coord(self, direction, center):
        """To get the coordinates of a footprint"""
        direction_list = self._direction_dict.get(direction)
        x = center.get_x() + direction_list[0]
        y = center.get_y() + direction_list[1]
        index = Index(x, y)
        return index

    def generate_destination(self, direction, destination):
        direction_list = self._direction_dict.get(direction)
        x = destination.get_x() + direction_list[0]
        y = destination.get_y() + direction_list[1]
        index = Index(x, y)
        return index

    def generate_all_piece_coords(self):
        coords_lst = []
        for direction, piece in self._direction_dict.items():
            coords_lst.append(self.generate_piece_coord(direction, self.get_center()))
        return coords_lst

    def validate_player_pieces(self, opposing_color):
        if self._center_piece == opposing_color:
            return False
        for direction, piece in self._footprint_ring.items():
            if piece == opposing_color:
                return False
        return True

    def get_footprint_coords(self):
        """Used to get all coordinates of each piece in a footprint"""
        return self._footprint_ring

    def __str__(self):
        """To convert the center coordinates from a string"""
        return self._center.__str__()


class Player:
    """Represents a player by colors Black or White. Will communicate with the GessGame class to determine
    the player's turn, and allow the player to resign, and update game state"""

    def __init__(self):
        """Initializes player 1 to Black and player 2 to White. Black makes the first move"""
        self._black = "B"
        self._white = "W"

    def get_player_turn(self):
        """Get the current player turn"""
        return self._player_turn

    def set_player_turn(self, player_turn):
        """Sets the current player's turn"""
        self._player_turn = player_turn


class Index:
    """Represents the coordinates of a footprint. Will communicate with the Board class to give the coordinates
    of each piece used. Set up as a class to use as an easy reference"""

    def __init__(self, x, y):
        """Initializes the x and y coordinates"""
        self._x = x
        self._y = y

    def get_x(self):
        """Gets the footprint's x coordinate"""
        return self._x

    def get_y(self):
        """Gets the footprint's y coordinate"""
        return self._y

    def __str__(self):
        """To help convert coordinates to strings"""
        return str(self._x) + " " + str(self._y)