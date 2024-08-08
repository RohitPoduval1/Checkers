from copy import deepcopy
from board import Board, EMPTY
from piece import Piece
from coordinate import Coordinate

BLACK = "BLACK"
RED = "RED"


class AI:
    def __init__(self) -> None:
        pass


    def result(self, board_obj: Board, piece: Piece, destination: Coordinate) -> list[list[Piece]]:
        """
        Return a temporary board that results from making action on the given board

        Args:
            board_obj (Board): the board object the game is played with
            piece (Piece): the piece to move
            destination (Coordinate): where the piece should be moved to

        Returns:
            The temporary board resulting from making move on the given board 
        """
        board_obj_copy = deepcopy(board_obj)

        board_obj_copy.move(piece, destination)
        return board_obj_copy._board


    def winner(self, board_obj: Board) -> str | None:
        """
        Given a board object, return the winner of the game
        """
        if board_obj.black_pieces_left == 0:
            return RED
        elif board_obj.red_pieces_left == 0:
            return BLACK
        else:
            return None


    def player_turn(self, board_obj: Board) -> str:
        return board_obj.current_turn


    def terminal(self, board_obj: Board) -> bool:
        """
        Given a board object, return whether the game is over
        """
        return board_obj.is_game_over()


    def moves(self, board_obj: Board, piece: Piece) -> set[Coordinate]:
        """
        Return a set of all possible moves available on the board for the given piece

        Args:
            board_obj (Board): the board object the game is played with
            piece (Piece): the piece to get moves for

        Returns:
            A set of Coordinates representing all possible moves for the given piece on the board 
        """
        return board_obj.all_valid_moves(piece)


    # BLACK - Maximizing player
    # red - minimizing player
    def utility(self, board_obj: Board) -> int:
        """
        Assign a value to each game state.

        Returns:
            An integer representing the game state's utility/value.
        """
        # A kinged piece will be worth 3 while a regular piece will be worth 1
        black_utility = board_obj.black_regular_left + (3 * board_obj.black_kings_left)

        # since RED is the minimizing player, have its utility be negative
        red_utility = -1 * (board_obj.red_regular_left + (3 * board_obj.red_kings_left))

        return black_utility + red_utility


    def minimax(self, board_obj: Board) -> Coordinate:
        if self.terminal(board_obj):
            return None

        best_move = None
        match self.player_turn(board_obj):
            # Maximizer
            case "BLACK":
                best_val = float("-inf")
                for piece in board_obj.pieces_with_valid_moves(self.player_turn(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = self.__min_value(self.result(board_obj, piece, move))
                        if val > best_val:
                            best_val = val
                            best_move = move

            # Minimizer
            case "RED":
                best_val = float("inf")
                for piece in board_obj.pieces_with_valid_moves(self.player_turn(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = self.__max_value(self.result(board_obj, piece, move))
                        if val < best_val:
                            best_val = val
                            best_move = move

        return best_move



    def __max_value(self, board_obj: Board) -> int:
        """Helper function to be used with the BLACK player in minimax"""
        if self.terminal(board_obj):
            return self.utility(board_obj)

        # Since BLACK is the maximizing player, we want to initialize the value to be the smallest
        # possible number since we are trying to get the largest number possible
        val = float("-inf")


        # Go through each piece on the board with the current color and see
        for piece in board_obj.pieces_with_valid_moves(self.player_turn(board_obj)):

            # What is the best possible move that will result in the highest possible utility value
            for move in self.moves(board_obj, piece):

                # given that the minimizing player is playing optimally?
                # Hence, MAX(current_val, min_value(resulting_board))
                val = max(val, self.__min_value(self.result(board_obj, piece, move)))
        return val


    def __min_value(self, board_obj: Board) -> int:
        """Helper function to be used with the RED player in minimax"""
        if self.terminal(board_obj):
            return self.utility(board_obj)

        # Since RED is the minimizing player, we want to initialize the value to be the largest
        # possible number since we are trying to get the smallest number possible
        val = float("inf")

        # Go through each piece on the board with the current color and see
        for piece in board_obj.pieces_with_valid_moves(self.player_turn(board_obj)):

            # What is the best possible move that will result in the highest possible utility value
            for move in self.moves(board_obj, piece):

                # given that the minimizing player is playing optimally?
                # Hence, MIN(current_val, max_value(resulting_board))
                val = min(val, self.__max_value(self.result(board_obj, piece, move)))
        return val
