from copy import deepcopy
from board import Board, EMPTY
from piece import Piece
from coordinate import Coordinate

BLACK = "BLACK"
RED = "RED"


class AI:
    def __init__(self) -> None:
        pass


    def result(self, board_obj: Board, piece: Piece, destination: Coordinate) -> Board:
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
        return board_obj_copy


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


    def player(self, board_obj: Board) -> str:
        """Return whose turn it is, either BLACK or RED"""
        return board_obj.current_turn


    def terminal(self, board_obj: Board) -> bool:
        """
        Given a board object, return whether the game is over.

        Returns:
            True if the game is over, False if it is not.
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


    def evaluate(self, board_obj: Board) -> int:
        """
        Assign a value to each game state based on the idea that BLACK is the maximizer
        and RED is the minimizer.

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
        best_piece = None

        def max_value(board_obj, alpha: int, beta: int) -> int:
            """
            Find the largest value of a game state with alpha beta pruning.

            Args:
                alpha (int): the best value so far along the game tree for the maximizing player 
                beta (int): the best value so far along the game tree for the minimizing player
            """
            if self.terminal(board_obj):
                return self.evaluate(board_obj)

            # Initialize with the worst case value to the maximizer so we always do better
            # with the first move so the algorithm can progress
            val = float("-inf")

            for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                for move in self.moves(board_obj, piece):
                    val = max(val, min_value(self.result(board_obj, piece, move), alpha, beta))
                    if val >= beta:
                        return val
                    alpha = max(alpha, val)
            return val

        def min_value(board_obj, alpha, beta) -> int:
            """
            Find the smallest value of a game state with alpha beta pruning.

            Args:
                alpha (int): the best value so far along the game tree for the maximizing player 
                beta (int): the best value so far along the game tree for the minimizing player
            """
            if self.terminal(board_obj):
                return self.evaluate(board_obj)

            # Initialize with the worst case value to the minimizer so we always do better
            # with the first move so the algorithm can progress
            v = float("inf")

            for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                for move in self.moves(board_obj, piece):
                    v = min(v, max_value(self.result(board_obj, piece, move), alpha, beta))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        match self.player(board_obj):
            # Maximizer
            case "BLACK":
                best_val = float("-inf")
                alpha = float("-inf")
                beta = float("inf")
                for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = min_value(self.result(board_obj, piece, move), alpha, beta)
                        if val > best_val and piece is not EMPTY:
                            best_val = val
                            best_move = move
                            best_piece = piece
                        alpha = max(alpha, best_val)

            # Minimizer
            case "RED":
                best_val = float("inf")
                alpha = float("-inf")
                beta = float("inf")
                for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = max_value(self.result(board_obj, piece, move), alpha, beta)
                        if val < best_val and piece is not EMPTY:
                            best_val = val
                            best_move = move
                            best_piece = piece
                        beta = min(beta, best_val)

        return (best_piece, best_move)
