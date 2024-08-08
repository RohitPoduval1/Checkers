import pygame
from board import EMPTY, Board, Coordinate
from constants import PIECE_BLACK
from constants import PIECE_RED


WINDOW_SIZE = 800  # one numbers since WINDOW should be square. Represents an 800x800 screen
FPS = 60
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Checkers")


def switch_player(current_turn: str, game_board):
    game_board.selected_piece = EMPTY
    game_board.reset_valid_moves()
    return "Black" if current_turn == "Red" else "Red"


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

    # 1x per game
    game_board.draw_grid(WINDOW)
    game_board.place_starting_pieces()

    current_turn = "Black"  # Black always goes first
    running = True
    while running:
        # ensure that the game runs at the same rate regardless of machine performance
        clock.tick(FPS)

        # Handle game overs
        is_game_over = game_board.is_game_over()
        if is_game_over:
            running = False
            winner = "Black" if game_board.winner() == "B" else "Red"
            print(f"The game is over! The winner is {winner}")

        for event in pygame.event.get():
            # Close button was pressed in top corner
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Use ESC key to end the game
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Choose the piece to be moved by either clicking or dragging
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coords = get_board_position_from_click(pygame.mouse.get_pos())

                # Conditions for selecting a piece
                mouse_piece = game_board.get_piece(mouse_coords)
                if (
                    mouse_piece is not EMPTY and  # select non-empty tiles on the board

                    # Select the piece that matches the current_turn color
                    (current_turn == "Black" and mouse_piece.color == PIECE_BLACK or
                    current_turn == "Red" and mouse_piece.color == PIECE_RED) and

                    mouse_piece in game_board.pieces_with_valid_moves(mouse_piece.color)
                ):
                    game_board.selected_piece = game_board.get_piece(mouse_coords)
                    game_board.selected_piece.king()

                    # populate valid_moves so they can be shown to the player
                    game_board.all_valid_moves(game_board.selected_piece)

            # Move the piece to the square where the mouse was released
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = get_board_position_from_click(pygame.mouse.get_pos())

                if game_board.selected_piece is not EMPTY:
                    start = Coordinate(game_board.selected_piece.row, game_board.selected_piece.col)
                    if game_board.move(game_board.selected_piece, mouse_coords):
                        # Check if the move was a jump
                        row_diff = mouse_coords.row - start.row
                        col_diff = mouse_coords.col - start.col
                        if abs(row_diff) == 2 and abs(col_diff) == 2:
                            # Handle multiple jumps
                            while True:
                                possible_jump_moves = game_board.find_single_jumps(game_board.selected_piece)

                                print("All valid moves: ")
                                [print(move) for move in game_board.all_valid_moves(game_board.selected_piece)]

                                print("All jump moves: ")
                                [print(move) for move in possible_jump_moves]
                                if possible_jump_moves:
                                    game_board._valid_moves = possible_jump_moves
                                else:
                                    current_turn = switch_player(current_turn, game_board)
                                break
                        else:
                            # Adjacent move, switch turn
                            current_turn = switch_player(current_turn, game_board)

        # Draw the board first and then the valid moves so that they properly show up on the board
        game_board.draw(WINDOW)
        # the valid moves are only drawn when the mouse is held down on a piece
        game_board.draw_valid_moves(WINDOW)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
