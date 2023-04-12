"""this code creates the player and computer player classes, as well as the game settings and functions.
This code is import only. The logic is handled in the main file."""

import numpy as np
import pygame
import sys

from numpy import ndarray

WIDTH, HEIGHT = 800, 800
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BOARD_SIZE = (3, 3)
OFFSET = 40


def draw_lines(screen):
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3, OFFSET), (WIDTH / 3, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 * 2, OFFSET), (WIDTH / 3 * 2, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT / 3), (WIDTH - OFFSET, HEIGHT / 3), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT / 3 * 2), (WIDTH - OFFSET, HEIGHT / 3 * 2), 5)


def start_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Tic-Tac-Toe")
    screen.fill(BG_COLOR)
    return screen


class Game:
    board: ndarray

    def __init__(self, screen: pygame.Surface):
        self.board = np.zeros((3, 3))
        self.size = BOARD_SIZE
        self.game_over = False
        self.winner = None
        self.new_game = True
        self.single_player = False
        self.multi_player = False
        self.screen = screen

    def mark_square(self, row_num, column, player_num):
        self.board[row_num][column] = player_num

    def available_square(self, row_num, column):
        return self.board[row_num][column] == 0

    def is_board_full(self):
        return not np.any(self.board == 0)

    def check_win(self):
        # Check horizontal locations for win
        for column in range(self.size[1]):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] and self.board[0][column] != 0:
                # draw win line
                pygame.draw.line(self.screen, LINE_COLOR, (column * WIDTH / 3 + WIDTH / 6, OFFSET),
                                 (column * WIDTH / 3 + WIDTH / 6, HEIGHT - OFFSET), 5)
                return self.board[0][column]

        # Check vertical locations for win
        for row in range(self.size[0]):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] != 0:
                # draw win line
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, row * HEIGHT / 3 + HEIGHT / 6),
                                 (WIDTH - OFFSET, row * HEIGHT / 3 + HEIGHT / 6), 5)
                return self.board[row][0]

        # Check diagonal locations for win
        if self.board[2][0] == self.board[1][1] == self.board[0][2] and self.board[2][0] != 0:
            # draw win line
            pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, HEIGHT - OFFSET), (WIDTH - OFFSET, OFFSET), 5)
            return self.board[1][1]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            # draw win line
            pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), 5)
            return self.board[1][1]

        return False

    def reset_game(self):
        self.board = np.zeros((3, 3))
        self.game_over = False
        self.winner = None
        self.screen.fill(BG_COLOR)
        draw_lines(self.screen)
        pygame.display.update()

    def new_game_menu(self, event, font):
        if self.new_game:
            self.screen.fill(BG_COLOR)
            text = font.render("Press 1 for single player, press 2 for multiplayer.", True, LINE_COLOR)
            self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.single_player = True
                    self.multi_player = False
                    self.new_game = False
                    self.reset_game()
                elif event.key == pygame.K_2:
                    self.multi_player = True
                    self.single_player = False
                    self.new_game = False
                    self.reset_game()


class Player:
    def __init__(self, player_num):
        self.player_num = player_num

    def get_player_num(self):
        return self.player_num
