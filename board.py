import pygame
from constants import GRID_BOX_SIZE, BOARD_RED, BOARD_BLACK, PIECE_RED, PIECE_BLACK
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
        self.SIZE = 8
        self._board = [[EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._selected_piece: Piece = EMPTY
        self._valid_moves: set[Coordinate] = set()
        self.black_pieces_left = 12
        self.red_pieces_left = 12


    def __str__(self) -> str:
        board_with_strings = [[" " for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for row in range(self.SIZE):
            for col in range(self.SIZE):
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
        return self._selected_piece


    @selected_piece.setter
    def selected_piece(self, piece):
        self._selected_piece = piece


    def select_piece(self, coord: Coordinate) -> None:
        """
        Make the piece at the given coordinates the selected piece if it is valid

        Args:
            coord (Coordinate): the location on the board to select
        """
        if self.get_piece(coord) is EMPTY:
            raise ValueError("There is no piece at (row, col) so no piece could be selected.")

        if self._selected_piece is not EMPTY:
            raise ValueError(
                "There is already a selected piece. Two pieces cannot be selected at the same time."
            )

        self._selected_piece = self.get_piece(coord)


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
        """
        Sets board at the given coordinates to piece

        Args:
            coord (Coordinate): coordinates of the board to change
            piece (Piece): the piece to set the board to 
        """
        self._board[coord.row][coord.col] = piece


    def place_starting_pieces(self) -> None:
        """Internally populates an empty board with the starting positions of the pieces"""
        # Draw the black pieces at the top of the board (the first 3 rows)
        for row in range(3):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_BLACK))

        # Draw the red pieces at the bottom of the board (the last 3 rows)
        for row in range(self.SIZE - 3, self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_RED))


    def draw_grid(self, window: pygame.Surface) -> None:
        """
        Draws a black and red checkerboard on the given window.
        
        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        window.fill(BOARD_BLACK)
        for r in range(self.SIZE):
            for c in range(r % 2, self.SIZE, 2):
                # Draw alternating red squares on the black board
                pygame.draw.rect(
                    surface=window,
                    color=BOARD_RED,
                    rect=(
                        r * GRID_BOX_SIZE,  # left
                        c * GRID_BOX_SIZE,  # top
                        GRID_BOX_SIZE,      # width
                        GRID_BOX_SIZE       # height
                    )
                )


    def draw(self, window: pygame.Surface) -> None:
        """
        Draws the current board, assumming the background is already drawn
        
        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        self.draw_grid(window)
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                piece = self.get_piece(Coordinate(row, col))
                if self.selected_piece is not EMPTY and self.selected_piece is piece:
                    self.__highlight_selected_piece_tile(window)
                if piece is not EMPTY:
                    piece.draw(window)


    def __highlight_selected_piece_tile(self, window: pygame.Surface) -> None:
        """
        Draw a yellow tile under the selected piece

        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        HIGHLIGHT_SQUARE_SIZE = GRID_BOX_SIZE * 0.8  # make it 80% the original size of the square

        # Draw the highlight box in the center of the tile that the selected_piece is in
        pygame.draw.rect(
            surface=window,
            color=(255, 223, 0),
            rect=(
                self.selected_piece.col*GRID_BOX_SIZE + (GRID_BOX_SIZE - HIGHLIGHT_SQUARE_SIZE)/2,
                self.selected_piece.row*GRID_BOX_SIZE + (GRID_BOX_SIZE - HIGHLIGHT_SQUARE_SIZE)/2,
                HIGHLIGHT_SQUARE_SIZE,
                HIGHLIGHT_SQUARE_SIZE
            )
        )


    def draw_valid_moves(self, window: pygame.Surface) -> None:
        """
        Draw a green circle on the board at each valid move to show it is valid.

        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        for valid_move in self._valid_moves:
            pygame.draw.circle(
                surface=window,
                color=(0, 240, 0),
                center=(
                    valid_move.col * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE,
                    valid_move.row * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE
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
            Boolean representing whether the move was successful
        """
        self.all_valid_moves(piece)
        if destination in self._valid_moves:
            start = Coordinate(piece.row, piece.col)

            # ALL MOVES
            self.set_board_at(start, EMPTY)  # clear the board at the old position

            # update that piece's position with the new row and column
            piece.row, piece.col = destination.row, destination.col

            # update the board to reflect the piece's new position
            self.set_board_at(destination, piece)
            piece.king()  # check if it is a king at the new position

            # JUMP MOVES
            row_diff, col_diff = destination.row - start.row, destination.col - start.col
            # if the move is a jump move
            if abs(row_diff) == 2 and abs(col_diff) == 2:
                # Adjust the respective piece count and remove the jumped piece from the board
                middle_piece_coords = Coordinate(start.row + row_diff//2, start.col + col_diff//2)
                if self.get_piece(middle_piece_coords).color == PIECE_BLACK:
                    self.black_pieces_left -= 1
                else:
                    self.red_pieces_left -= 1
                self.set_board_at(middle_piece_coords, EMPTY)

            return True  # since the move was valid

        return False


    def _is_valid_move(self, piece: Piece, destination: Coordinate) -> bool:
        """
        Check whether moving piece to destination is valid while doing necessary error checking.

        Args:
            piece (Piece): the piece to move
            destination (Piece): the destination to valid

        Return:
            True if the move is valid, False otherwise
        """
        start = Coordinate(piece.row, piece.col)

        # ERROR CHECKING
        if (
            # the start or destination is not a valid coordinate
            (not (start.is_in_bounds() and destination.is_in_bounds())) or

            # there is no valid piece to move or the destination has a piece
            (piece is EMPTY or self.get_piece(destination) is not EMPTY)
        ):
            return False

        # ADJACENT MOVEMENT
        row_diff = destination.row - start.row
        col_diff = destination.col - start.col

        # row_diff must be positive for black since it moves down and negative for red since it
        # moves up while col diff can be either (+, -) for black and red since they can move
        # left or right.
        if (
            ((piece.color == PIECE_BLACK or piece.is_king) and row_diff == 1 and abs(col_diff) == 1) or
            ((piece.color == PIECE_RED or piece.is_king) and row_diff == -1 and abs(col_diff) == 1)
        ):
            return True

        # JUMPING MOVEMENT
        middle_row = start.row + row_diff // 2
        middle_col = start.col + col_diff // 2
        middle_piece = self.get_piece(Coordinate(middle_row, middle_col))

        # Ensure there is an opponent's piece in the middle
        if middle_piece is not EMPTY and middle_piece.color != piece.color:
            # If the jump is valid given the piece (color, is_king), return True
            if (
                ((piece.color == PIECE_BLACK or piece.is_king) and row_diff == 2 and abs(col_diff) == 2) or
                ((piece.color == PIECE_RED or piece.is_king) and row_diff == -2 and abs(col_diff) == 2)
            ):
                return True

        return False


    def all_single_jumps(self, piece: Piece) -> set[Coordinate]:
        """
        Get all the valid single jumps for the given piece.

        Args:
            piece (Piece): the piece to inspect jumps for

        Returns:
            A set of Coordinates representing the valid jumps possible with the piece
        """
        valid_jump_moves: set[Coordinate] = set()
        jump_directions = []

        if piece.color == PIECE_BLACK or piece.is_king:
            jump_directions.append( (2, -2) )  # down-left
            jump_directions.append( (2, 2) )   # down-right
        if piece.color == PIECE_RED or piece.is_king:
            jump_directions.append( (-2, -2) )  # up-left
            jump_directions.append( (-2, 2) )   # up-right

        for row_diff, col_diff in jump_directions:
            jump_destination = Coordinate(piece.row + row_diff, piece.col + col_diff)
            if self._is_valid_move(piece, jump_destination):
                valid_jump_moves.add(jump_destination)

        return valid_jump_moves


    def find_adjacent_moves(self, piece: Piece) -> set[Coordinate]:
        """
        Given a valid piece, return all possible adjacent moves
    
        Args:
            piece (Piece): Must be a valid piece, meaning not EMPTY

        Returns:
            A set of Coordinates representing the valid adjacent moves possible with the piece
        """
        directions = []

        # Populate directions with movement options that are valid for the given piece
        # based on its color and king status.
        if piece.color == PIECE_BLACK or piece.is_king:
            directions.append((1, -1))  # down-left
            directions.append((1, 1))   # down-right
        if piece.color == PIECE_RED or piece.is_king:
            directions.append((-1, -1))  # up-left
            directions.append((-1, 1))   # up-right

        adjacent_moves = set()
        # With the directions for the given piece, check all of them and add the ones that
        # are valid to the set.
        for row_diff, col_diff in directions:
            destination = Coordinate(piece.row + row_diff, piece.col + col_diff)
            if self._is_valid_move(piece, destination):
                adjacent_moves.add(destination)

        return adjacent_moves


    def all_valid_moves(self, piece: Piece) -> set[Coordinate]:
        """
        Given a valid piece, returns all valid moves that piece has available to it.

        Args:
            piece (Piece): Must be a valid piece, meaning not EMPTY

        Returns:
            A set of Coordinates representing all valid moves possible with the piece
        """
        adjacent_moves = self.find_adjacent_moves(piece)
        jump_moves = self.all_single_jumps(piece)

        # if a jump is possible, it must be made
        if len(jump_moves) > 0:
            self._valid_moves = jump_moves

        # otherwise, no jumps are possible so take adjacent moves
        else:
            self._valid_moves = adjacent_moves

        return self._valid_moves


    def pieces_with_valid_moves(self, color) -> set[Piece]:
        # TODO: Add to README detailed explanation on mandatory jumping
        """
        Return a set of Pieces of the specified color that have valid moves available to it.
        This is important because the rules of checkers states that if there exists a piece on
        the board with a jump available to it, it must make the jump. If multiple pieces exist
        with jumps available, then the player can choose.

        Args:
            color: the color of the piece to search for valid moves, either PIECE_BLACK or PIECE_RED

        Returns:
            A set of Pieces, each with valid moves available to it
        """
        pieces = set()

        # See if there are any pieces on the board matching the passed in color
        # that have available jump moves
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(Coordinate(r, c))
                if (
                    piece is not EMPTY and
                    len(self.all_single_jumps(piece)) > 0 and
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
                        len(self.find_adjacent_moves(piece)) > 0 and
                        piece.color == color
                    ):
                        pieces.add(piece)
        return pieces


    def is_game_over(self) -> bool:
        return self.black_pieces_left == 0 or self.red_pieces_left == 0

    def winner(self) -> str:
        """Return the winner of the game, 'B' for black or 'R' for red"""
        return "B" if self.red_pieces_left == 0 else "R"
