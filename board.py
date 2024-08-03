import pygame
from constants import GRID_BOX_SIZE, BOARD_RED, BOARD_BLACK, PIECE_RED, PIECE_BLACK
from piece import Piece


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
        self._selected_piece = EMPTY

    def __str__(self) -> str:
        board_with_strings = [[" " for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                curr_piece = self.get_piece(row, col)
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
        return self._selected_piece

    @selected_piece.setter
    def selected_piece(self, piece):
        """If piece is a valid piece, it makes it the selected_piece"""
        self._selected_piece = piece


    def get_piece(self, row: int, col) -> Piece:
        """Returns the piece at a given row and col if it exists.
        Otherwise, based on the initialization of the board, it will return EMPTY"""
        return self.board[row][col]

    def set_board_at(self, row: int, col: int, piece) -> None:
        """Sets board at row, col to piece"""
        self.board[row][col] = piece

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

    def draw_starting_pieces(self, window: pygame.Surface):
        """Draws the starting position of the pieces

        Args:
            window (pygame.Surface): the window to draw the grid on
        """
        # Draw the black pieces at the top of the board (the first 3 rows)
        for row in range(3):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # Place on alternating squares
                    self.set_board_at(row, col, Piece(row, col, PIECE_BLACK))
                    self.get_piece(row, col).draw(window)

        # Draw the red pieces at the bottom of the board (the last 3 rows)
        for row in range(self.SIZE - 3, self.SIZE):
            for col in range(self.SIZE):
                if (row + col) % 2 == 1:  # Place on alternating squares
                    self.set_board_at(row, col, Piece(row, col, PIECE_RED))
                    self.get_piece(row, col).draw(window)

    def erase_at(self, row: int, col: int, window: pygame.Surface) -> None:
        """To be called when moving a piece. Updates the board visually to reflect that a piece
        has been moved by drawing the corresponding colored square where the piece was.

        Args:
            row (int): the row in which the piece was previously located. The row of the square
            to be erased.
            col (int): the column in which the piece was previously located. The column of the 
            square to be erased.
            window (pygame.Surface): the surface where the erase should be displayed
        """
        square_color = BOARD_RED if (row + col) % 2 == 0 else BOARD_BLACK
        pygame.draw.rect(
            surface=window,
            color=square_color,
            rect=(col * GRID_BOX_SIZE, row * GRID_BOX_SIZE, GRID_BOX_SIZE, GRID_BOX_SIZE)
        )

    def move(self, piece, row: int, col: int, window: pygame.Surface):
        """Moves piece to row, col and updates the board both internally and visually
        by drawing the piece on the board using window.

        Args: 
            piece (Piece): the piece to move
            row (int): the new row to move the piece to
            col (int): the new column to move the piece to
            window: the window to draw on
        """

        # To move a piece, we must first check if there is a piece to move
        if self.get_piece(piece.row, piece.col) is EMPTY:
            raise ValueError("Piece argument is None. There is no piece to move")
        # Also check if the destination is empty
        if self.get_piece(row, col) is not EMPTY:
            raise ValueError("The destination is not empty, there is already a piece there.")

        # Clear the board at the old position
        self.set_board_at(piece.row, piece.col, EMPTY)  # update the board internally
        self.erase_at(piece.row, piece.col, window)     # and visually.

        # Update that piece's position with the new row and column
        piece.row = row
        piece.col = col

        # Update the board to reflect the piece's new position
        self.set_board_at(row, col, piece)     # internally
        self.get_piece(row, col).draw(window)  # visually

    def select_piece(self, row: int, col: int) -> None:
        """Gets the piece at row, col on the board (if valid) and makes it the selected piece"""
        if self.get_piece(row, col) is EMPTY:
            raise ValueError("There is no piece at (row, col) so no piece could be selected.")

        if self._selected_piece is not EMPTY:
            raise ValueError(
                "There is already a selected piece. Two pieces cannot be selected at the same time."
            )

        # Made it through all the checks so the piece can be selected
        self._selected_piece = self.get_piece(row, col)
