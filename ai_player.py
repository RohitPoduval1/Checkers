from copy import deepcopy
from board import Board
from piece import Piece
from coordinate import Coordinate

BLACK = "BLACK"
RED = "RED"


class AI:
    def __init__(self) -> None:
        pass


    def minimax(self, game_state: Board) -> tuple[Piece, Coordinate]:
        """
        Given a Board, return the best possible move for the AI player

        Args:
            game_state (Board): the Board object the game is being played on

        Returns:
            A tuple consisting of the piece to move and where that piece should be moved
            in that order.
        """
        if game_state.is_game_over():
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
        match game_state.current_turn:
            # Maximizer
            case "BLACK":
                best_val = float("-inf")

                for piece in game_state.pieces_with_valid_moves(color=game_state.current_turn):
                    for move in game_state.get_valid_moves(piece):
                        val = self.__min_value(
                            self.__result(game_state, piece, move),
                            alpha,
                            beta,
                            depth=look_moves_ahead
                        )

                        # Store the best action available so far
                        if val > best_val:
                            best_val = val
                            best_move = move
                            best_piece = piece

                        alpha = max(alpha, best_val)

            # Minimizer
            case "RED":
                best_val = float("inf")
                for piece in game_state.pieces_with_valid_moves(color=game_state.current_turn):
                    for move in game_state.get_valid_moves(piece):
                        val = self.__max_value(
                            self.__result(game_state, piece, move),
                            alpha,
                            beta,
                            depth=look_moves_ahead
                        )

                        # Store the best action available so far
                        if val < best_val:
                            best_val = val
                            best_move = move
                            best_piece = piece

                        beta = min(beta, best_val)

        return (best_piece, best_move)


    def __min_value(self, game_state, alpha: int, beta: int, depth: int) -> int:
        """
        Find the smallest value of a game state with alpha beta pruning.
        Helper function for minimax()

        Args:
            alpha (int): the best value so far along the game tree for the maximizing player 
            beta (int): the best value so far along the game tree for the minimizing player
        """
        if game_state.is_game_over() or depth == 0:
            return self.__evaluate(game_state)

        # Initialize with the worst case value to the minimizer so we always do better
        # with the first move so the algorithm can progress
        min_val = float("inf")

        for piece in game_state.pieces_with_valid_moves(game_state.current_turn):
            for move in game_state.get_valid_moves(piece):
                min_val = min(
                    min_val,
                    self.__max_value(
                        self.__result(game_state, piece, move),
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


    def __max_value(self, game_state, alpha: int, beta: int, depth: int) -> int:
        """
        Find the largest value of a game state with alpha beta pruning.
        Helper function for minimax()

        Args:
            alpha (int): the best value so far along the game tree for the maximizing player 
            beta (int): the best value so far along the game tree for the minimizing player
        """
        if game_state.is_game_over() or depth == 0:
            return self.__evaluate(game_state)

        # Initialize with the worst case value to the maximizer so we always do better
        # with the first move so the algorithm can progress
        max_val = float("-inf")

        for piece in game_state.pieces_with_valid_moves(game_state.current_turn):
            for move in game_state.get_valid_moves(piece):
                max_val = max(
                    max_val,
                    self.__min_value(
                        self.__result(game_state, piece, move),
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


    def __result(self, game_state: Board, piece: Piece, destination: Coordinate) -> Board:
        """
        Return a temporary board that results from making action on the given board

        Args:
            game_state (Board): the board object the game is played with
            piece (Piece): the piece to move
            destination (Coordinate): where the piece should be moved to

        Returns:
            The temporary board __resulting from making move on the given board. The original board
            is not altered.
        """
        # We don't want to alter any part of the given board so we copy the board and piece
        # since move() changes both of them
        game_state_copy = deepcopy(game_state)
        piece_copy = deepcopy(piece)

        game_state_copy.move(piece_copy, destination)
        game_state_copy.switch_player()
        return game_state_copy


    def __evaluate(self, game_state: Board) -> int:
        """
        Assign a value to each game state based on the idea that Black is the maximizer and RED
        is the minimizer. A value greater than 0 favors Black while a value less than 0 favors RED.
        0 means that neither Black nor Red has the advantage.

        Returns:
            An integer representing the game state's utility/value.
        """
        # A king will be worth 3 while a regular piece will be worth 1
        black_utility = game_state.black_regular_left + (3 * game_state.black_kings_left)

        # since RED is the minimizing player, have its utility be negative
        red_utility = -1 * (game_state.red_regular_left + (3 * game_state.red_kings_left))

        return black_utility + red_utility

