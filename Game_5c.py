import random
import pygame
import sys
from pygame.locals import *

# Board: (List (List Color))
# A Board is a 2-D list of colors

# A Color is a [List Int, Int, Int]
# - Where each position represents the RGB
GRAY = (100, 100, 100)
NAVY_BLUE = (60,  60, 100)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
PURPLE = (255,   0, 255)
CYAN = (0, 255, 255)
ALL_COLORS = [GRAY, NAVY_BLUE, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_WIDTH = 5
BOARD_HEIGHT = 4
BOX_SIZE = 50
GAP_SIZE = 10
WIDTH_MARGIN = int(((WINDOW_WIDTH - ((BOX_SIZE * BOARD_WIDTH) + (GAP_SIZE * (BOARD_WIDTH - 1)))) / 2))
HEIGHT_MARGIN = int((WINDOW_HEIGHT - ((BOX_SIZE * BOARD_HEIGHT) + (GAP_SIZE * (BOARD_HEIGHT - 1)))) / 2)
RADIUS = int(BOX_SIZE / 2)
FPS = 60

DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS_CLOCK = pygame.time.Clock()

BG_COLOR = (0, 0, 0)


def main():
    pygame.init()
    main_board = get_random_board()
    revealed_boxes = no_revealed_boxes()
    first_selection = None
    second_selection = None
    DISPLAY.fill(WHITE)
    mouse_column = 0
    mouse_row = 0

    while True:
        mouse_clicked = False
        DISPLAY.fill(BG_COLOR)
        draw_board(main_board, revealed_boxes)

        # Checking if the User exit out the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_column, mouse_row = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_column, mouse_row = event.pos
                mouse_clicked = True

        # Check to see if both selections are correct
        if second_selection is not None and first_selection is not None:
            if check_if_correct(main_board, first_selection[0], first_selection[1],
                                second_selection[0], second_selection[1]) is True:
                first_selection = None
                second_selection = None
            else:
                pygame.display.update()
                pygame.time.wait(1000)
                revealed_boxes[first_selection[0]][first_selection[1]] = False
                revealed_boxes[second_selection[0]][second_selection[1]] = False
                first_selection = None
                second_selection = None

        # Update based on clicking
        box_row, box_column = convert_pixel_to_box(mouse_column, mouse_row)
        if (box_column is not None and box_row is not None) and mouse_clicked is True:
            if (first_selection is None and second_selection is None) and revealed_boxes[box_row][box_column] is False:
                first_selection = box_row, box_column
                revealed_boxes[box_row][box_column] = True
            elif (first_selection is not None and second_selection is None) and revealed_boxes[box_row][box_column] is \
                    False:
                second_selection = box_row, box_column
                revealed_boxes[box_row][box_column] = True

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

# Drawing Function -----------------------------------------------------------------------------------------------------


# draw_board: Board (List (List Boolean)) -> Image
def draw_board(board, revealed):
    for box_column in range(BOARD_WIDTH):
        for box_row in range(BOARD_HEIGHT):
            if not revealed[box_row][box_column]:
                draw_box(box_row, box_column)
            else:
                draw_icon(board, box_row, box_column)


# draw_box: Int Int -> Image
# Purpose: When given the box coordinates, it will create a box
def draw_box(box_row, box_column):
    top, left = get_left_top_of_box(box_row, box_column)
    pygame.draw.rect(DISPLAY, WHITE, (left, top, BOX_SIZE, BOX_SIZE))


# get_left_top_of_box: Int Int -> (Int Int)
# Purpose: When given the box coordinates, it will give the pixel coordinates of the top left of the box
def get_left_top_of_box(box_row, box_column):
    left = int(WIDTH_MARGIN + (box_column * (BOX_SIZE + GAP_SIZE)))
    top = int(HEIGHT_MARGIN + (box_row * (BOX_SIZE + GAP_SIZE)))
    return top, left


# draw_icon: Board, Int, Int: Image
# Purpose: When given a board and the box coordinates, it will create the icon under that box
def draw_icon(board, box_row, box_column):
    row, column = get_left_top_of_box(box_row, box_column)
    row = int(row + (BOX_SIZE / 2))
    column = int(column + (BOX_SIZE / 2))
    pygame.draw.circle(DISPLAY, board[box_row][box_column], (column, row), RADIUS, 0)


# Mouse Function -------------------------------------------------------------------------------------------------------


# convert_pixel_to_box: Int, Int -> (Int, Int)
# Purpose: It will take in the coordinates of the mouse and see if there are any boxes that collide with that coordinate
#          If so, it will return the box coordinates. If not, it will return (None, None)
def convert_pixel_to_box(mouse_column, mouse_row):
    for box_column in range(BOARD_WIDTH):
        for box_row in range(BOARD_HEIGHT):
            top, left = get_left_top_of_box(box_row, box_column)
            rectangle = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if rectangle.collidepoint(mouse_column, mouse_row):
                return box_row, box_column
    return None, None


# Checker Function -----------------------------------------------------------------------------------------------------

def check_if_correct(board, boxx_1, boxy_1, boxx_2, boxy_2):
    return board[boxx_1][boxy_1] == board[boxx_2][boxy_2]

# Start-Up Functions ---------------------------------------------------------------------------------------------------


# get_random_board: No Input -> Board
# Purpose: To generate a random board with the board width and height as the dimensions
def get_random_board():
    number_of_icons_used = int(BOARD_HEIGHT * BOARD_WIDTH / 2)
    colors_available = ALL_COLORS[:number_of_icons_used] * 2
    random.shuffle(colors_available)

    board = []
    for box_x in range(BOARD_HEIGHT):
        column = []
        for box_y in range(BOARD_WIDTH):
            column.append(colors_available[0])
            del colors_available[0]
        board.append(column)
    return board


# no_revealed_boxes: No Input -> (List (List Boolean))
# Purpose: To create a 2-D array that has the dimensions of the board width and height and have all the elements
#          as False.
def no_revealed_boxes():
    revealed_boxes = []
    for x in range(BOARD_HEIGHT):
        revealed_boxes.append([False] * BOARD_WIDTH)
    return revealed_boxes


main()

