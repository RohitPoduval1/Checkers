import pygame 
from constants import GRID_BOX_SIZE

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
    def is_king(self, is_king: bool) -> None:
        self.is_king = is_king

    def king(self) -> None:
        """Make a piece a king"""
        self.is_king = True

    def draw(self, window: pygame.Surface) -> None:
        """Draws the piece on the specified window"""
        if self.is_king:
            # TODO: Draw a different image for a kinged piece
            pass
        else:
            pygame.draw.circle(
                surface=window,
                color=self._COLOR,
                center=(
                    self._col * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE,  # use col to find x coord
                    self._row * GRID_BOX_SIZE + 0.5*GRID_BOX_SIZE   # use row to find y coord
                ),
                radius=Piece.RADIUS
            )
