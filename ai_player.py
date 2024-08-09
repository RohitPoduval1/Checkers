from copy import deepcopy
from board import Board
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
        # We don't want to alter any part of the given board so we copy the board and piece
        # since move() changes both of them
        board_obj_copy = deepcopy(board_obj)
        piece_copy = deepcopy(piece)

        board_obj_copy.move(piece_copy, destination)
        board_obj_copy.switch_player()
        return board_obj_copy


    def winner(self, board_obj: Board) -> str | None:
        """
        Given a board object, return the winner of the game

        Returns:
            "BLACK" if Black won, "RED" if Red won, None otherwise
        """
        if board_obj.black_pieces_left == 0:
            return RED
        if board_obj.red_pieces_left == 0:
            return BLACK
        return None


    def player(self, board_obj: Board) -> str:
        """Return whose turn it is, either 'BLACK' or 'RED'"""
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
        return board_obj.get_valid_moves(piece)


    def evaluate(self, board_obj: Board) -> int:
        """
        Assign a value to each game state based on the idea that BLACK is the maximizer
        and RED is the minimizer.

        Returns:
            An integer representing the game state's utility/value.
        """
        # A king will be worth 3 while a regular piece will be worth 1
        black_utility = board_obj.black_regular_left + (3 * board_obj.black_kings_left)

        # since RED is the minimizing player, have its utility be negative
        red_utility = -1 * (board_obj.red_regular_left + (3 * board_obj.red_kings_left))

        return black_utility + red_utility



    def minimax(self, board_obj: Board) -> Coordinate:
        if self.terminal(board_obj):
            return None

        # Keep track of the best move that can be made and which piece can make that move
        best_move = None
        best_piece = None

        alpha=float("-inf")  # the best value so far for the max player
        beta=float("inf")    # the best value so far for the min player

        # As part of Depth-Limited Minimax, we limit how far the AI looks ahead to save time
        # 5 moves ahead is fairly quick
        # 6 moves ahead takes slightly longer
        # Anything above 8 is impractical (and not fun) to wait for
        look_moves_ahead = 5
        match self.player(board_obj):
            # Maximizer
            case "BLACK":
                best_val = float("-inf")
                for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = self.min_value(
                            self.result(board_obj, piece, move),
                            alpha,
                            beta,
                            depth=look_moves_ahead
                        )
                        if val > best_val:
                            best_val = val
                            best_move = move
                            best_piece = piece

                        alpha = max(alpha, best_val)

            # Minimizer
            case "RED":
                best_val = float("inf")
                for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
                    for move in self.moves(board_obj, piece):
                        val = self.max_value(
                            self.result(board_obj, piece, move),
                            alpha,
                            beta,
                            depth=look_moves_ahead
                        )
                        if val < best_val:
                            best_val = val
                            best_move = move
                            best_piece = piece
                        beta = min(beta, best_val)

        return (best_piece, best_move)


    def min_value(self, board_obj, alpha: int, beta: int, depth: int) -> int:
        """
        Find the smallest value of a game state with alpha beta pruning.
        Helper function for minimax()

        Args:
            alpha (int): the best value so far along the game tree for the maximizing player 
            beta (int): the best value so far along the game tree for the minimizing player
        """
        if self.terminal(board_obj) or depth == 0:
            return self.evaluate(board_obj)

        # Initialize with the worst case value to the minimizer so we always do better
        # with the first move so the algorithm can progress
        min_val = float("inf")

        for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
            for move in self.moves(board_obj, piece):
                min_val = min(
                    min_val,
                    self.max_value(
                        self.result(board_obj, piece, move),
                        alpha,
                        beta,
                        depth - 1
                    )
                )

                # Alpha Beta Pruning
                beta = min(beta, min_val)
                if beta <= alpha:
                    break
        return min_val


    def max_value(self, board_obj, alpha: int, beta: int, depth: int) -> int:
        """
        Find the largest value of a game state with alpha beta pruning.
        Helper function for minimax()

        Args:
            alpha (int): the best value so far along the game tree for the maximizing player 
            beta (int): the best value so far along the game tree for the minimizing player
        """
        if self.terminal(board_obj) or depth == 0:
            return self.evaluate(board_obj)

        # Initialize with the worst case value to the maximizer so we always do better
        # with the first move so the algorithm can progress
        max_val = float("-inf")

        for piece in board_obj.pieces_with_valid_moves(self.player(board_obj)):
            for move in self.moves(board_obj, piece):
                max_val = max(
                    max_val,
                    self.min_value(
                       self.result(board_obj, piece, move),
                        alpha,
                        beta,
                        depth - 1
                    )
                )

                # Alpha Beta Pruning
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break
        return max_val
