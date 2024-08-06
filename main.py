import pygame
from board import EMPTY, Board, Coordinate


WINDOW_SIZE = 800  # one numbers since WINDOW should be square. Represents an 800x800 screen
FPS = 60
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Checkers")


def get_board_position_from_click(mouse_coord: int):
    """Given a mouse coordinate, return the corresponding position on the board.
    
    Args:
        mouse_cord (int): either the mouse's x position or y position

    Returns:
        the board's row if mouse_y is given; board's column if mouse_x is given
        mouse_row = get_board_position_from_click(mouse_y)
        mouse_col = get_board_position_from_click(mouse_x)
    """
    # The hundreds digit of the mouse coordinates, mouse_x and mouse_y
    # correspond to the column and row respectively the mouse is located in

    # subtract whatever needed to make a number cleanly divisible by 100
    # divide that number by 100 to get the hundreds digit
    return (mouse_coord - (mouse_coord % 100)) // 100 if mouse_coord > 100 else 0


def main():
    """Function where main game loop occurs. All classes come together in this function."""
    clock = pygame.time.Clock()
    game_board = Board()

    # 1x per game
    game_board.draw_grid(WINDOW)
    game_board.place_starting_pieces()
    game_board.draw(WINDOW)

    running = True
    while running:

        # ensure that the game runs at the same rate regardless of machine performance
        clock.tick(FPS)

        for event in pygame.event.get():

            # Close button was pressed in top corner
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Use ESC key to end the game
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_coords = Coordinate(
                    row=get_board_position_from_click(mouse_y),
                    col=get_board_position_from_click(mouse_x)
                )
                # only attempt to get pieces from non empty board squares
                if game_board.get_piece(mouse_coords) is not EMPTY:
                    game_board.selected_piece = game_board.get_piece(mouse_coords)
                    game_board.all_valid_moves(game_board.selected_piece)


            if event.type == pygame.MOUSEBUTTONUP:
                # Move the piece on the square that the mouse was released
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_coords = Coordinate(
                    row=get_board_position_from_click(mouse_y),
                    col=get_board_position_from_click(mouse_x)
                )

                game_board.move(game_board.selected_piece, mouse_coords)
                game_board.selected_piece = EMPTY
                game_board.valid_moves = set()


            if event.type == pygame.MOUSEMOTION:
                pass


        game_board.draw(WINDOW)
        game_board.draw_valid_moves(WINDOW)
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
