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
        self.board = [[EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._selected_piece: Piece = EMPTY
        self.valid_moves: set[Coordinate] = set()

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
        """If piece is a valid piece, it makes it the selected_piece"""
        self._selected_piece = piece

    def select_piece(self, coord: Coordinate) -> None:
        """Gets the piece at the given coordinates on the board (if valid) and makes it
        the selected piece"""
        if self.get_piece(coord) is EMPTY:
            raise ValueError("There is no piece at (row, col) so no piece could be selected.")

        if self._selected_piece is not EMPTY:
            raise ValueError(
                "There is already a selected piece. Two pieces cannot be selected at the same time."
            )

        # Made it through all the checks so the piece can be selected
        self._selected_piece = self.get_piece(coord)

    def get_piece(self, coord: Coordinate) -> Piece:
        """Returns the piece at the given coordinates' row and col if it exists.
        Otherwise, based on the initialization of the board, it will return EMPTY"""
        return self.board[coord.row][coord.col]

    def set_board_at(self, coord: Coordinate, piece) -> None:
        """Sets board at the given coordinates to piece"""
        self.board[coord.row][coord.col] = piece

    def draw_grid(self, window: pygame.Surface):
        """Draws a black and red checkerboard on the given window.
        To be called once at the beginning of the game
        
        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        window.fill(BOARD_BLACK)
        for r in range(self.SIZE):
            for c in range(r % 2, self.SIZE, 2):
                pygame.draw.rect(
                    surface=window,
                    color=BOARD_RED,
                    # (left, top, width, height)
                    rect=(r * GRID_BOX_SIZE, c * GRID_BOX_SIZE, GRID_BOX_SIZE, GRID_BOX_SIZE)
                )

    def place_starting_pieces(self):
        """Populates an empty board with the starting positions of the pieces"""
        # Draw the black pieces at the top of the board (the first 3 rows)
        for row in range(3):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # Place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_BLACK))

        # Draw the red pieces at the bottom of the board (the last 3 rows)
        for row in range(self.SIZE - 3, self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # Place on alternating squares
                    self.set_board_at(Coordinate(row, col), Piece(row, col, PIECE_RED))

    def draw(self, window):
        """Draws the current board, assumming the background is already drawn"""
        self.draw_grid(window)
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                coords = Coordinate(row, col)
                if self.get_piece(coords) is not EMPTY:
                    self.get_piece(coords).draw(window)

    def draw_valid_moves(self, window: pygame.Surface) -> None:
        """Given a set of valid moves, draw a green circle on the board at each valid move to show it is valid"""
        for valid_move in self.valid_moves:
            pygame.draw.circle(
                surface=window,
                color=(0, 240, 0),
                center=(
                    valid_move.col * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE,  # use col to find x coord
                    valid_move.row * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE   # use row to find y coord
                ),
                radius=15
            )

    def _erase_at(self, coord: Coordinate, window: pygame.Surface) -> None:
        """To be called when moving a piece. Updates the board visually to reflect that a piece
        has been moved by drawing the corresponding colored square where the piece was.
        """
        square_color = BOARD_RED if (coord.row + coord.col) % 2 == 0 else BOARD_BLACK
        pygame.draw.rect(
            surface=window,
            color=square_color,
            rect=(
                coord.col * GRID_BOX_SIZE,
                coord.row * GRID_BOX_SIZE,
                GRID_BOX_SIZE,
                GRID_BOX_SIZE
            )
        )

    def move(self, piece, destination: Coordinate):
        """Moves piece to destination and updates the board internally. 

        Args: 
            piece (Piece): the piece to move
            destination (Coordinate): the destination of the piece
        """
        if self.is_valid_move(piece, destination):
            start = Coordinate(piece.row, piece.col)
            # Clear the board at the old position
            self.set_board_at(start, EMPTY)

            # Update that piece's position with the new row and column
            piece.row = destination.row
            piece.col = destination.col

            # update the board to reflect the piece's new position
            self.set_board_at(destination, piece)


    def is_valid_move(self, piece: Piece, destination: Coordinate) -> bool:
        start = Coordinate(piece.row, piece.col)

        # ERROR CHECKING
        # The destination must be a valid coordinate
        if not (start.is_in_bounds() and destination.is_in_bounds()):
            return False

        # Invalid if there is no piece to move or the destination already has a piece
        if piece is EMPTY or self.get_piece(destination) is not EMPTY:
            return False

        # ADJACENT MOVEMENT
        row_diff = destination.row - start.row
        col_diff = destination.col - start.col

        # For black movement, row_diff must be positive since black moves down, col diff can be either
        if (piece.color == PIECE_BLACK or piece.is_king) and row_diff == 1 and abs(col_diff) == 1:
            return True

        # For red movement, row_diff must be negative since red moves down, col_diff can be either
        if (piece.color == PIECE_RED or piece.is_king) and row_diff == -1 and abs(col_diff) == 1:
            return True

        # JUMPING MOVEMENT
        middle_row = start.row + row_diff // 2
        middle_col = start.col + col_diff // 2
        middle_piece = self.get_piece(Coordinate(middle_row, middle_col))

        # Ensure there is an opponent's piece in the middle
        if middle_piece is not EMPTY and middle_piece.color != piece.color:
            if (piece.color == PIECE_BLACK or piece.is_king) and row_diff == 2 and abs(col_diff) == 2:
                return True
            if (piece.color == PIECE_RED or piece.is_king) and row_diff == -2 and abs(col_diff) == 2:
                return True

        return False

    def all_valid_moves(self, piece: Piece) -> set:
        """Given a piece, returns all valid moves that piece has available to it"""
        self.valid_moves = set()
        start = Coordinate(piece.row, piece.col)

        directions = []
        if piece.color == PIECE_BLACK or piece.is_king:
            directions.append((1, -1))  # Down-left
            directions.append((1, 1))   # Down-right
        if piece.color == PIECE_RED or piece.is_king:
            directions.append((-1, -1))  # Up-left
            directions.append((-1, 1))   # Up-right

        # Check adjacent moves
        for row_diff, col_diff in directions:
            destination = Coordinate(start.row + row_diff, start.col + col_diff)
            if self.is_valid_move(piece, destination):
                self.valid_moves.add(destination)

        # Check for jumps
        def find_jumps(piece, start, visited):
            for row_diff, col_diff in directions:
                jump_destination = Coordinate(start.row + 2*row_diff, start.col + 2*col_diff)

                if jump_destination not in visited and self.is_valid_move(piece, jump_destination):
                    self.valid_moves.add(jump_destination)
                    visited.add(jump_destination)

                    # Temporarily update piece's position to check for further jumps
                    original_position = Coordinate(piece.row, piece.col)
                    self.set_board_at(original_position, EMPTY)
                    self.set_board_at(jump_destination, piece)
                    piece.row, piece.col = jump_destination.row, jump_destination.col

                    # check for further jumps
                    find_jumps(piece, jump_destination, visited)

                    # Revert the temporary move
                    piece.row, piece.col = original_position.row, original_position.col
                    self.set_board_at(jump_destination, EMPTY)
                    self.set_board_at(original_position, piece)

        # start finding jumps from the initial position
        find_jumps(piece, start, set())

        return self.valid_moves
