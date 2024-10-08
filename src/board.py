import pygame
from constants import BOARD_RED, BOARD_BLACK, PIECE_RED, PIECE_BLACK
from constants import SQUARE_SIZE, DIMENSIONS
from piece import Piece
from coordinate import Coordinate


EMPTY = None


class Board:
    """Connects the pieces (the Piece class) with the board the user sees.
    
    Attributes:
        size (int): the dimensions of the board. A checkers board is an 8x8 grid
        board: a 2D array of Pieces used as a simplified representation of the board.
    """
    def __init__(self):
        self._board = [[EMPTY for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]
        self.__selected_piece: Piece = EMPTY
        self._valid_moves: set[Coordinate] = set()

        self.black_regular_left = 12
        self.black_kings_left = 0
        self.black_pieces_left = self.black_regular_left + self.black_kings_left

        self.red_regular_left = 12
        self.red_kings_left = 0
        self.red_pieces_left = self.red_regular_left + self.red_kings_left

        self._current_turn = "BLACK"


    def __str__(self) -> str:
        board_with_strings = [[" " for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]
        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                curr_piece = self.get_piece(Coordinate(row, col))
                piece_as_string = ""
                if curr_piece.color == PIECE_RED:
                    piece_as_string += "R"
                    if curr_piece.is_king:
                        piece_as_string += "K"
                elif curr_piece.color == PIECE_BLACK:
                    piece_as_string += "B"
                    if curr_piece.is_king:
                        piece_as_string += "K"
                board_with_strings[row][col] = piece_as_string

        board_as_string = ""
        for row in board_with_strings:
            line = "".join(row)
            board_as_string += (f"{line} \n")

        return board_as_string


    @property
    def selected_piece(self):
        """Getter for selected_piece attribute"""
        return self.__selected_piece

    @selected_piece.setter
    def selected_piece(self, piece):
        self.__selected_piece = piece


    @property
    def current_turn(self):
        """Getter for current_turn attribute"""
        return self._current_turn

    @current_turn.setter
    def current_turn(self, next_turn: str):
        self._current_turn = next_turn


    def select_piece(self, coord: Coordinate) -> None:
        """
        Make the piece at the given coordinates the selected piece if it is valid

        Args:
            coord (Coordinate): the location on the board to select
        """
        self.__selected_piece = self.get_piece(coord)


    def reset_valid_moves(self) -> None:
        """Make the set of valid moves empty"""
        self._valid_moves = set()


    def get_piece(self, coord: Coordinate) -> Piece:
        """
        Returns the piece at the given coordinates' row and col if it exists.
        Otherwise, based on the initialization of the board, it will return EMPTY

        Args:
            coord (Coordinate): the coordinates on the board to get from

        Returns:
            The piece at the coordinates. Either a valid piece or EMPTY
        """
        return self._board[coord.row][coord.col]


    def set_board_at(self, coord: Coordinate, piece: Piece) -> None:
        """Sets board at the given coordinates to piece"""
        self._board[coord.row][coord.col] = piece


    def place_starting_pieces(self) -> None:
        """Internally populates an empty board with the starting positions of the pieces"""
        # Draw the black pieces at the top of the board (the first 3 rows)
        for row in range(3):
            for col in range(DIMENSIONS):
                if (row + col) % 2 == 1:  # place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_BLACK))

        # Draw the red pieces at the bottom of the board (the last 3 rows)
        for row in range(DIMENSIONS - 3, DIMENSIONS):
            for col in range(DIMENSIONS):
                if (row + col) % 2 == 1:  # place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_RED))


    def draw_checkerboard(self, window: pygame.Surface) -> None:
        """Draw a black and red checkerboard on the given window."""
        window.fill(BOARD_BLACK)

        # Draw alternating red squares on the black board to make a checkerboard
        for r in range(DIMENSIONS):
            for c in range(r % 2, DIMENSIONS, 2):
                pygame.draw.rect(
                    surface=window,
                    color=BOARD_RED,
                    rect=(
                        r * SQUARE_SIZE,  # left
                        c * SQUARE_SIZE,  # top
                        SQUARE_SIZE,      # width
                        SQUARE_SIZE       # height
                    )
                )


    def draw(self, window: pygame.Surface) -> None:
        """Draw the current board on the given window"""

        # Get rid of existing drawings by drawing the checkerboard on top,
        # effectively giving us a clean slate to work with.
        self.draw_checkerboard(window)

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                piece = self.get_piece(Coordinate(row, col))
                if self.selected_piece is not EMPTY and piece is self.selected_piece:
                    self.__highlight_selected_piece_tile(window)
                if piece is not EMPTY:
                    piece.draw(window)




    def draw_valid_moves(self, window: pygame.Surface) -> None:
        """Draw a green circle on the board at each valid move to show it is valid."""
        if self.selected_piece is not EMPTY:
            for valid_move in self._valid_moves:
                pygame.draw.circle(
                    surface=window,
                    color=(0, 240, 0),
                    center=(
                        valid_move.col * SQUARE_SIZE + 0.5*SQUARE_SIZE,
                        valid_move.row * SQUARE_SIZE + 0.5*SQUARE_SIZE
                    ),
                    radius=15
                )


    def move(self, piece: Piece, destination: Coordinate) -> bool:
        """
        Moves piece to destination and updates the board internally. 

        Args: 
            piece (Piece): the piece to move
            destination (Coordinate): the destination of the piece

        Returns:
            True if move was successful, False otherwise
        """
        self.get_valid_moves(piece)
        if destination not in self._valid_moves:
            return False

        move_type = self.get_move_type(piece, destination)
        if move_type == "JUMP":
            row_diff = destination.row - piece.row
            col_diff = destination.col - piece.col
            middle_piece_coords = Coordinate(piece.row + row_diff//2, piece.col + col_diff//2)
            middle_piece = self.get_piece(middle_piece_coords)

            if middle_piece.color == PIECE_BLACK:
                if middle_piece.is_king:
                    self.black_kings_left -= 1
                else:
                    self.black_regular_left -= 1
                self.black_pieces_left -= 1
            else:
                if middle_piece.is_king:
                    self.red_kings_left -= 1
                else:
                    self.red_regular_left -= 1
                self.red_pieces_left -= 1
            self.set_board_at(middle_piece_coords, EMPTY)

        self.set_board_at(piece, EMPTY)  # clear the board at the old position

        # update that piece's position with the new row and column
        piece.row, piece.col = destination.row, destination.col

        self.set_board_at(destination, piece)

        # If the piece is a newly made king, update the number of pieces left
        if piece.king():
            if piece.color == PIECE_BLACK:
                self.black_regular_left -= 1
                self.black_kings_left += 1
            else:
                self.red_regular_left -= 1
                self.red_kings_left += 1
        self.black_pieces_left = self.black_regular_left + self.black_kings_left
        self.red_pieces_left = self.red_regular_left + self.red_kings_left

        return True


    def get_move_type(self, piece: Piece, destination: Coordinate) -> str | None:
        """
        Given a Piece and its destination, return whether that move is an
        adjacent move, jump move, or none.

        Args:
            piece (Piece): the piece making the potential move
            destination (Coordinate): where the piece is moving to

        Returns:
            'ADJACENT' if the move is an adjacent move or 'JUMP' if the move jumps a piece.
            Otherwise, return None.
        """
        row_diff, col_diff = destination.row - piece.row, destination.col - piece.col

        # row_diff must be positive for black since it moves down and negative for red since it
        # moves up while col diff can be either (+, -) for black and red since they can move
        # left or right.
        if abs(col_diff) == 1 and (
            (piece.is_king) or
            (piece.color == PIECE_BLACK and row_diff == 1) or
            (piece.color == PIECE_RED and row_diff == -1)
        ):
            return "ADJACENT"

        if abs(col_diff) == 2 and (
            (piece.is_king) or
            (piece.color == PIECE_BLACK and row_diff == 2) or
            (piece.color == PIECE_RED and row_diff == -2)
        ):
            return "JUMP"

        return None


    def get_single_jumps(self, piece: Piece) -> set[Coordinate]:
        """
        Get all the valid single jumps for the given piece.

        Args:
            piece (Piece): the piece to inspect jumps for

        Returns:
            A set of Coordinates representing the valid jumps possible with the piece
        """
        jump_moves: set[Coordinate] = set()
        jump_directions = []

        if piece.color == PIECE_BLACK or piece.is_king:
            jump_directions.append( (2, -2) )  # down-left
            jump_directions.append( (2, 2) )   # down-right
        if piece.color == PIECE_RED or piece.is_king:
            jump_directions.append( (-2, -2) )  # up-left
            jump_directions.append( (-2, 2) )   # up-right

        for row_diff, col_diff in jump_directions:
            jump_destination = Coordinate(piece.row + row_diff, piece.col + col_diff)
            if self.__is_valid_move(piece, jump_destination):
                jump_moves.add(jump_destination)

        return jump_moves




    def get_valid_moves(self, piece: Piece) -> set[Coordinate]:
        """
        Given a valid piece, returns all valid moves that piece has available to it.

        Args:
            piece (Piece): Must be a valid piece, meaning not EMPTY

        Returns:
            A set of Coordinates representing all valid moves possible with the piece
        """
        adjacent_moves = self.__get_adjacent_moves(piece)
        jump_moves = self.get_single_jumps(piece)

        # if a jump is possible, it must be made
        if len(jump_moves) > 0:
            self._valid_moves = jump_moves

        # otherwise, no jumps are possible so take adjacent moves
        else:
            self._valid_moves = adjacent_moves

        return self._valid_moves


    def pieces_with_valid_moves(self, color) -> set[Piece]:
        """
        Return a set of Pieces of the specified color that have valid moves available to it.

        Args:
            color: the color of the piece to search for valid moves, either PIECE_BLACK or PIECE_RED

        Returns:
            A set of Pieces, each with valid moves available to it
        """
        pieces = set()
        if color in [PIECE_BLACK, PIECE_RED]:
            pass
        else:
            color = PIECE_BLACK if color == "BLACK" else PIECE_RED


        # See if there are any pieces on the board matching the passed in color
        # that have available jump moves
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(Coordinate(r, c))
                if (
                    piece is not EMPTY and
                    len(self.get_single_jumps(piece)) > 0 and
                    piece.color == color
                ):
                    pieces.add(piece)

        # There are no pieces with jumps available so just get pieces with valid adjacent moves
        if len(pieces) == 0:
            for r in range(8):
                for c in range(8):
                    piece = self.get_piece(Coordinate(r, c))
                    if (
                        piece is not EMPTY and
                        len(self.__get_adjacent_moves(piece)) > 0 and
                        piece.color == color
                    ):
                        pieces.add(piece)
        return pieces


    def switch_player(self) -> None:
        """Switch whose turn it is. 'BLACK' becomes 'RED' and vice versa."""
        self.selected_piece = EMPTY
        self.reset_valid_moves()

        if self.current_turn == "BLACK":
            self.current_turn = "RED"
        else:
            self.current_turn = "BLACK"


    def is_game_over(self) -> bool:
        """
        Determine whether the game is over.
        
        Returns:
            True if the game is over and False if it is not.
        """
        return self.black_pieces_left == 0 or self.red_pieces_left == 0


    def winner(self) -> str:
        """
        Determine the winner of the game if the game has already been determined to be over.

        Returns:
            'BLACK' if Black won the game, 'RED' otherwise.
        """
        return "BLACK" if self.red_pieces_left == 0 else "RED"


    def __is_valid_move(self, piece: Piece, destination: Coordinate) -> bool:
        """
        Check whether moving piece to destination is valid while doing necessary error checking.

        Args:
            piece (Piece): the piece to move
            destination (Piece): the destination to valid

        Return:
            True if the move is valid, False otherwise
        """
        start = Coordinate(piece.row, piece.col)

        if (
            # the start or destination is not a valid coordinate
            (not (start.is_in_bounds() and destination.is_in_bounds())) or

            # there is no valid piece to move or the destination has a piece
            (piece is EMPTY or self.get_piece(destination) is not EMPTY)
        ):
            return False

        if self.get_move_type(piece, destination) == "ADJACENT":
            return True

        # Jumping Movement
        row_diff = destination.row - start.row
        col_diff = destination.col - start.col
        middle_row = start.row + row_diff // 2
        middle_col = start.col + col_diff // 2
        middle_piece = self.get_piece(Coordinate(middle_row, middle_col))

        if (
            self.get_move_type(piece, destination) == "JUMP" and
            middle_piece is not EMPTY and
            middle_piece.color != piece.color
        ):
            return True

        return False


    def __highlight_selected_piece_tile(self, window: pygame.Surface) -> None:
        """
        Draw a yellow tile under the selected piece

        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        HIGHLIGHT_SQUARE_SIZE = SQUARE_SIZE * 0.8  # make it 80% the original size of the square

        # Draw the highlight box in the center of the square that the selected_piece is in
        pygame.draw.rect(
            surface=window,
            color=(255, 223, 0),
            rect=(
                self.selected_piece.col*SQUARE_SIZE + (SQUARE_SIZE - HIGHLIGHT_SQUARE_SIZE)/2,
                self.selected_piece.row*SQUARE_SIZE + (SQUARE_SIZE - HIGHLIGHT_SQUARE_SIZE)/2,
                HIGHLIGHT_SQUARE_SIZE,
                HIGHLIGHT_SQUARE_SIZE
            )
        )


    def __get_adjacent_moves(self, piece: Piece) -> set[Coordinate]:
        """
        Given a valid piece, return all possible adjacent moves
    
        Args:
            piece (Piece): Must be a valid piece, meaning not EMPTY

        Returns:
            A set of Coordinates representing the valid adjacent moves possible with the piece
        """
        directions = []

        if piece.color == PIECE_BLACK or piece.is_king:
            directions.append((1, -1))  # down-left
            directions.append((1, 1))   # down-right
        if piece.color == PIECE_RED or piece.is_king:
            directions.append((-1, -1))  # up-left
            directions.append((-1, 1))   # up-right

        adjacent_moves = set()
        for row_diff, col_diff in directions:
            destination = Coordinate(piece.row + row_diff, piece.col + col_diff)
            if self.__is_valid_move(piece, destination):
                adjacent_moves.add(destination)

        return adjacent_moves
