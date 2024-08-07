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

        # Made it through all the checks so the piece can be selected
        self._selected_piece = self.get_piece(coord)

    def reset_valid_moves(self):
        self._valid_moves = set()

    def get_piece(self, coord: Coordinate) -> Piece:
        """Returns the piece at the given coordinates' row and col if it exists.
        Otherwise, based on the initialization of the board, it will return EMPTY"""
        return self._board[coord.row][coord.col]

    def set_board_at(self, coord: Coordinate, piece: Piece) -> None:
        """Sets board at the given coordinates to piece"""
        self._board[coord.row][coord.col] = piece


    def place_starting_pieces(self):
        """Internally populates an empty board with the starting positions of the pieces"""
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

    def draw_grid(self, window: pygame.Surface):
        """
        Draws a black and red checkerboard on the given window.
        
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

    def draw(self, window):
        """Draws the current board, assumming the background is already drawn"""
        self.draw_grid(window)
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                piece = self.get_piece(Coordinate(row, col))
                if self.selected_piece is not EMPTY and self.selected_piece is piece:
                    self._highlight_selected_piece_tile(window)
                if piece is not EMPTY:
                    # king any pieces since draw() is called constantly in the main game loop
                    piece.king()
                    piece.draw(window)

    def _highlight_selected_piece_tile(self, window: pygame.Surface) -> None:
        HIGHLIGHT_SQUARE_SIZE = GRID_BOX_SIZE * 0.8

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
        """Given a set of valid moves, draw a green circle on the board at each valid move to show it is valid"""
        for valid_move in self._valid_moves:
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

    def move(self, piece: Piece, destination: Coordinate) -> bool:
        """Moves piece to destination and updates the board internally. 

        Args: 
            piece (Piece): the piece to move
            destination (Coordinate): the destination of the piece
        """
        self.all_valid_moves(piece)
        if destination in self._valid_moves:
            start = Coordinate(piece.row, piece.col)
            # clear the board at the old position
            self.set_board_at(start, EMPTY)

            # Update that piece's position with the new row and column
            piece.row = destination.row
            piece.col = destination.col

            # update the board to reflect the piece's new position
            self.set_board_at(destination, piece)

            # Removing the jumped piece for jump moves
            row_diff = destination.row - start.row
            col_diff = destination.col - start.col
            if abs(row_diff) == 2 and abs(col_diff) == 2:  # if the move is a jump move
                middle_piece_coords = Coordinate(start.row + row_diff//2, start.col + col_diff//2)
                if self.get_piece(middle_piece_coords).color == PIECE_BLACK:
                    self.black_pieces_left -= 1
                else:
                    self.red_pieces_left -= 1
                self.set_board_at(middle_piece_coords, EMPTY)

            return True
        return False

    def _is_valid_move(self, piece: Piece, destination: Coordinate) -> bool:
        """
        Returns whether moving piece to destination is valid while doing necessary error checking.

        Args:
            piece (Piece): the piece to move
            destination (Piece): the destination to valid
        """
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

        # For black movement, row_diff must be positive since black moves down
        # while col diff can be either for both black and red since you can move left or right
        if (piece.color == PIECE_BLACK or piece.is_king) and row_diff == 1 and abs(col_diff) == 1:
            return True

        # For red movement, row_diff must be negative since red moves down
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


    def find_single_jumps(self, piece: Piece) -> set[Coordinate]:
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
        """Given a valid piece, return all possible adjacent moves"""
        directions = []
        if piece.color == PIECE_BLACK or piece.is_king:
            directions.append((1, -1))  # down-left
            directions.append((1, 1))   # down-right
        if piece.color == PIECE_RED or piece.is_king:
            directions.append((-1, -1))  # up-left
            directions.append((-1, 1))   # up-right

        adjacent_moves = set()
        # Check adjacent moves
        for row_diff, col_diff in directions:
            destination = Coordinate(piece.row + row_diff, piece.col + col_diff)
            if self._is_valid_move(piece, destination):
                adjacent_moves.add(destination)

        return adjacent_moves

    def all_valid_moves(self, piece: Piece) -> set[Coordinate]:
        """Given a valid piece, returns all valid moves that piece has available to it"""
        adjacent_moves = self.find_adjacent_moves(piece)
        jump_moves = self.find_single_jumps(piece)

        # The official rules of Checkers states that if a jump is possible, it must be made
        if len(jump_moves) > 0:
            self._valid_moves = jump_moves
        else:
            self._valid_moves = adjacent_moves

        return self._valid_moves

    def pieces_with_valid_moves(self, color) -> set[Piece]:
        # TODO: Add to README detailed explanation on mandatory jumping
        """
        Return a set of Pieces of color that have valid moves available to it. This is important
        because the rules of checkers states that if there exists a piece on the board with a jump
        available to it, it must make the jump. If multiple pieces exist with jumps available, then
        the player can choose.

        Args:
            color: the color of the piece to search for valid moves, either PIECE_BLACK or PIECE_RED

        Returns: a set of Pieces with valid moves available to it
        """
        pieces = set()

        # See if there are any pieces on the board matching the passed in color
        # that have available jump moves
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(Coordinate(r, c))
                if (
                    piece is not EMPTY and
                    len(self.find_single_jumps(piece)) > 0 and
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
                        len(self.all_valid_moves(piece)) > 0 and
                        piece.color == color
                    ):
                        pieces.add(piece)
        return pieces


    def is_game_over(self) -> bool:
        return self.black_pieces_left == 0 or self.red_pieces_left == 0

    def winner(self) -> str:
        """Return the winner of the game, 'B' for black or 'R' for red"""
        return "B" if self.red_pieces_left == 0 else "R"
