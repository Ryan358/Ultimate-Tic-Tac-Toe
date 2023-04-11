"""A simple tic-tac-toe game in pygame, made for two players."""

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 800, 800
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BOARD_SIZE = (3, 3)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BG_COLOR)

board = np.zeros(BOARD_SIZE)

GAME_OVER = False
player = 1
# sysfont = pygame.font.get_default_font()
# print('system font :', sysfont)
font = pygame.font.SysFont(None, 40)


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3, 10), (WIDTH / 3, HEIGHT - 10), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 * 2, 10), (WIDTH / 3 * 2, HEIGHT - 10), 5)
    pygame.draw.line(screen, LINE_COLOR, (10, HEIGHT / 3), (WIDTH - 10, HEIGHT / 3), 5)
    pygame.draw.line(screen, LINE_COLOR, (10, HEIGHT / 3 * 2), (WIDTH - 10, HEIGHT / 3 * 2), 5)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    return not np.any(board == 0)


def check_win():
    # Check horizontal locations for win
    for col in range(BOARD_SIZE[1]):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            # draw win line
            pygame.draw.line(screen, LINE_COLOR, (col * WIDTH / 3 + WIDTH / 6, 10),
                             (col * WIDTH / 3 + WIDTH / 6, HEIGHT - 10), 5)
            return board[0][col]

    # Check vertical locations for win
    for row in range(BOARD_SIZE[0]):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != 0:
            # draw win line
            pygame.draw.line(screen, LINE_COLOR, (10, row * HEIGHT / 3 + HEIGHT / 6),
                             (WIDTH - 10, row * HEIGHT / 3 + HEIGHT / 6), 5)
            return board[row][0]

    # Check diagonal locations for win
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != 0:
        # draw win line
        pygame.draw.line(screen, LINE_COLOR, (10, HEIGHT - 10), (WIDTH - 10, 10), 5)
        return board[1][1]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        # draw win line
        pygame.draw.line(screen, LINE_COLOR, (10, 10), (WIDTH - 10, HEIGHT - 10), 5)
        return board[1][1]

    return False


def draw_figures(pos: tuple, player: int):
    if player == 1:
        pygame.draw.circle(screen, LINE_COLOR, pos, 60, 15)
    else:
        pygame.draw.line(screen, LINE_COLOR, (pos[0] - 60, pos[1] - 60), (pos[0] + 60, pos[1] + 60), 15)
        pygame.draw.line(screen, LINE_COLOR, (pos[0] + 60, pos[1] - 60), (pos[0] - 60, pos[1] + 60), 15)


def reset_game():
    global GAME_OVER, board
    board = np.zeros(BOARD_SIZE)
    GAME_OVER = False

    screen.fill(BG_COLOR)
    draw_lines()



draw_lines()

while True:
    for event in pygame.event.get():
        if check_win():
            text = font.render(f"Player {player} wins!", True, LINE_COLOR)
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, text.get_height() / 2))
            GAME_OVER = True
        if is_board_full():
            GAME_OVER = True
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
            x, y = pygame.mouse.get_pos()

            if x < WIDTH / 3:
                col = 0
            elif x < WIDTH / 3 * 2:
                col = 1
            elif x < WIDTH:
                col = 2
            else:
                col = None

            if y < HEIGHT / 3:
                row = 0
            elif y < HEIGHT / 3 * 2:
                row = 1
            elif y < HEIGHT:
                row = 2
            else:
                row = None

            if row is not None and col is not None and available_square(row, col):
                mark_square(row, col, player)
                # center the x's and o's in each box
                figure_x = (col * WIDTH / 3) + WIDTH / 6
                figure_y = (row * HEIGHT / 3) + HEIGHT / 6

                draw_figures((figure_x, figure_y), player)
                if player == 1:
                    player = 2
                else:
                    player = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        if GAME_OVER:
            restart_text = font.render("Press R to restart", True, LINE_COLOR)
            screen.blit(restart_text, (WIDTH / 3 - restart_text.get_width() , HEIGHT - restart_text.get_height()))
            quit_text = font.render("Press SPACE to quit", True, LINE_COLOR)
            screen.blit(quit_text, (WIDTH  - quit_text.get_width(), HEIGHT - quit_text.get_height()))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit("Thanks for playing!")

    pygame.display.update()
