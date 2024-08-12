import pygame
from board import EMPTY, Board, Coordinate
from constants import PIECE_BLACK, PIECE_RED
from ai_player import AI


WINDOW_SIZE = 800  # one numbers since WINDOW should be square. Represents an 800x800 screen
FPS = 60
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Checkers")


def switch_player(current_turn: str, game_board):
    game_board.selected_piece = EMPTY
    game_board.reset_valid_moves()
    return "BLACK" if current_turn == "RED" else "RED"


def get_board_position_from_click(mouse_coords: tuple[int, int]):
    """Given a mouse coordinate, return the corresponding position on the board as a Coordinate.
    
    Args:
        mouse_coords (tuple[int, int]): should be passing in pygame.mouse.get_pos()
        mouse_coords[0] is the row of the mouse and mouse_coords[1] is the column

    Returns:
        a Coordinate object representing which tile the mouse is on
    """
    # The hundreds digit of the mouse coordinates, mouse_x and mouse_y, correspond to the column
    # and row respectively the mouse is located in.

    # Subtract whatever needed to make a number cleanly divisible by 100.
    # Divide that number by 100 to get the hundreds digit.
    row = (mouse_coords[1] - (mouse_coords[1] % 100)) // 100 if mouse_coords[1] > 100 else 0
    col = (mouse_coords[0] - (mouse_coords[0] % 100)) // 100 if mouse_coords[0] > 100 else 0

    return Coordinate(row, col)


def main():
    """Function where main game loop occurs. All classes come together in this function."""
    clock = pygame.time.Clock()
    game_board = Board()
    ai = AI()

    PLAYER_COLOR = "BLACK"
    AI_COLOR = "RED"

    # 1x per game
    game_board.draw_checkerboard(WINDOW)
    game_board.place_starting_pieces()

    running = True
    while running:
        # ensure that the game runs at the same rate regardless of machine performance
        clock.tick(FPS)

        # Handle game overs
        is_game_over = game_board.is_game_over()
        if is_game_over:
            running = False
            print(f"The game is over! The winner is {game_board.winner()}")
            break

        # AI Player
        if game_board.current_turn == AI_COLOR:
            ai_piece, ai_destination = ai.minimax(game_board)
            move_type = game_board.get_move_type(ai_piece, ai_destination)
            if game_board.move(ai_piece, ai_destination):
                if move_type == "ADJACENT":
                    game_board.switch_player()
                elif move_type == "JUMP":
                    while True:
                        possible_jump_moves = game_board.get_single_jumps(ai_piece)
                        if possible_jump_moves:
                            game_board.move(ai_piece, possible_jump_moves.pop())
                        else:
                            game_board.switch_player()
                            break


        for event in pygame.event.get():
            # Close button was pressed in top corner
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Use ESC key to end the game
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Handle clicks for both selecting and moving pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_board_coords = get_board_position_from_click(pygame.mouse.get_pos())
                mouse_piece = game_board.get_piece(mouse_board_coords)

                if PLAYER_COLOR == "BLACK":
                    player_piece_color = PIECE_BLACK
                else:
                    player_piece_color = PIECE_RED

                # Covers selecting pieces, both when one is not selected and when one is selected
                # but the player wants to change
                if (
                    mouse_piece is not EMPTY and
                    (game_board.current_turn == PLAYER_COLOR and mouse_piece.color == player_piece_color) and
                    mouse_piece in game_board.pieces_with_valid_moves(player_piece_color)
                ):
                    game_board.select_piece(mouse_piece)
                    game_board.get_valid_moves(game_board.selected_piece)

                # Moving a selected piece to an empty square
                elif game_board.selected_piece is not EMPTY and mouse_piece is EMPTY:
                    move_type = game_board.get_move_type(game_board.selected_piece, mouse_board_coords)
                    if game_board.move(game_board.selected_piece, mouse_board_coords):
                        if move_type == "JUMP":
                            while True:
                                possible_jump_moves = game_board.get_single_jumps(game_board.selected_piece)
                                if possible_jump_moves:
                                    game_board._valid_moves = possible_jump_moves
                                else:
                                    game_board.switch_player()
                                break
                        else:
                            game_board.switch_player()
                    else:
                        game_board.selected_piece = None


        # Draw the board first and then the valid moves so that they properly show up on the board
        game_board.draw(WINDOW)
        # the valid moves are only drawn when a piece is selected
        game_board.draw_valid_moves(WINDOW)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

