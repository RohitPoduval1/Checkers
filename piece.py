import pygame 
from constants import GRID_BOX_SIZE, PIECE_BLACK, PIECE_RED
from coordinate import Coordinate

class Piece:
    """Represents a piece in checkers.
    
    Attributes:
        row (int): the current row of the board that the piece is on
        col (int): the current column of the board that the piece is on
        is_king (bool): whether the piece is a king or not. This allows for movement
        in all 4 diagonal directions
        color: which side/team the piece is on, either red or black. 
        
    """
    RADIUS = 38

    def __init__(self, r: int, c: int, color):
        """
        Args:
            r (int): the row that the piece should be placed in 
            c (int): the column that the piece should be placed in
            color: which side the piece is, either red or black
        """
        self._row = r
        self._col = c
        self._is_king = False
        self._COLOR = color

    def __eq__(self, other_piece) -> bool:
        return (
            self.row == other_piece.row and
            self.col == other_piece.col and
            self.color == other_piece.color and
            self.is_king == other_piece.is_king
        )

    def __hash__(self) -> int:
        color_int = 1 if self.color == "PIECE_BLACK" else -1
        return self.row + self.col + color_int

    def __str__(self) -> str:
        color_str = "Black" if self.color == PIECE_BLACK else "Red"
        king_str = "King" if self.is_king else "Piece"
        return f"{color_str} {king_str} at {Coordinate(self.row, self.col)}"

    @property
    def row(self) -> int:
        """Getter for row attribute"""
        return self._row

    @property
    def col(self) -> int:
        """Getter for col attribute"""
        return self._col

    @property
    def is_king(self) -> bool:
        """Getter for is_king attribute"""
        return self._is_king

    @property
    def color(self):
        """Getter for COLOR attribute"""
        return self._COLOR

    @row.setter
    def row(self, r: int) -> None:
        self._row = r

    @col.setter
    def col(self, c: int) -> None:
        self._col = c

    @is_king.setter
    def is_king(self, k):
        self._is_king = k

    def king(self) -> None:
        """Make a piece a king if the conditions are met"""
        if (self.color == PIECE_BLACK and self.row == 7) or (self.color == PIECE_RED and self.row == 0):
            self._is_king = True

    def draw(self, window: pygame.Surface) -> None:
        """Draws the piece on the specified window"""
        # TODO: Draw a different image for a kinged piece
        pygame.draw.circle(
            surface=window,
            color=self._COLOR,
            center=(
                self._col * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE,  # use col to find x coord
                self._row * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE   # use row to find y coord
            ),
            radius=Piece.RADIUS
        )
