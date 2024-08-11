import pygame 
from constants import SQUARE_SIZE, PIECE_BLACK, PIECE_RED
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
        self.__row = r
        self.__col = c
        self.__is_king = False
        self.__COLOR = color

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
        return self.__row

    @property
    def col(self) -> int:
        """Getter for col attribute"""
        return self.__col

    @property
    def is_king(self) -> bool:
        """Getter for is_king attribute"""
        return self.__is_king

    @property
    def color(self):
        """Getter for COLOR attribute"""
        return self.__COLOR

    @row.setter
    def row(self, r: int) -> None:
        self.__row = r

    @col.setter
    def col(self, c: int) -> None:
        self.__col = c

    @is_king.setter
    def is_king(self, k):
        self.__is_king = k

    def king(self) -> bool:
        """
        Make a piece a king if it is not already and the conditions are met.

        Returns:
            True if the piece was made king for the first time, False if the conditions were not
            met or the piece is already a king.
        """
        if ((self.color == PIECE_BLACK and self.row == 7) or (self.color == PIECE_RED and self.row == 0)) and not self.is_king:
            self.__is_king = True
            return self.__is_king
        return False

    def draw(self, window: pygame.Surface) -> None:
        """Draws the piece on the specified window. If the piece is a king, draw a crown for it"""
        pygame.draw.circle(
            surface=window,
            color=self.__COLOR,
            center=(
                self.__col * SQUARE_SIZE + 0.5*SQUARE_SIZE,  # use col to find x coord
                self.__row * SQUARE_SIZE + 0.5*SQUARE_SIZE   # use row to find y coord
            ),
            radius=Piece.RADIUS
        )
        if self.is_king:
            crown_image = pygame.image.load("assets/crown.png")

            # Draw the crown in the center of the piece
            crown_image_rect = pygame.Rect(
                (self.col*SQUARE_SIZE + 0.5*SQUARE_SIZE) - (crown_image.get_width() // 2),
                (self.row*SQUARE_SIZE + 0.5*SQUARE_SIZE) - (crown_image.get_height() // 2),
                crown_image.get_width(),
                crown_image.get_height()
            )
            window.blit(crown_image, crown_image_rect)
