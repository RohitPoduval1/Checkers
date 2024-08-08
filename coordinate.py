class Coordinate:
    """
    A clean, concise way of representing a coordinate pair consisting of (row, column)
    specifically based on the checkerboard's dimensions. 
    
    Attributes:
        row (int): the row of the piece on the checkerboard
        col (int): the column of the piece on the checkerboard
    """
    def __init__(self, row, col) -> None:
        self._row = row
        self._col = col

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __hash__(self):
        # Since sets are a hash-based collection, a consistent way of hashing should be used.
        # The default returns an integer based on the object's instance, not value. This should
        # be overriden to be based on the value so that two Coordinates that are the same based on
        # __eq__ should return the same hash value
        return hash((self.row, self.col))

    @property
    def row(self):
        """Getter for row attribute"""
        return self._row

    @property
    def col(self):
        """Getter for column attribute"""
        return self._col

    @row.setter
    def row(self, r):
        self._row = r

    @col.setter
    def col(self, c):
        self._col = c


    def is_in_bounds(self):
        """Check whether the coordinates are in the bounds of the board"""
        # TODO: Get rid of hardcoded 8 and replace with board.SIZE
        return (
            0 <= self._row < 8 and
            0 <= self._col < 8
        )
