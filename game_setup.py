"""This code creates the player and computer player classes, as well as the game settings and functions.
This code is import only. The logic is handled in the main file."""

import numpy as np
import pygame
import random
from numpy import ndarray
import math
import time

WIDTH, HEIGHT = 800, 800
BG_COLOR = (220, 220, 220)
LINE_COLOR = (0, 0, 0)
BOARD_SIZE = (3, 3)
OFFSET = 40
delay = 0.5


def draw_lines(screen: pygame.Surface):
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
        self.player_turn = 1
        self.simulated_board = False

    def mark_square(self, row_num: int, column: int, player_num: int):
        self.board[row_num][column] = player_num

    def unmark_square(self, row_num: int, column: int):
        self.board[row_num][column] = 0

    def available_square(self, row_num: int, column: int):
        return self.board[row_num][column] == 0

    def is_board_full(self):
        return not np.any(self.board == 0)

    def check_win(self):
        # Check horizontal locations for win
        for column in range(self.size[1]):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] and self.board[0][column] != 0:
                # draw win line if not simulated
                if not self.simulated_board:
                    pygame.draw.line(self.screen, LINE_COLOR, (column * WIDTH / 3 + WIDTH / 6, OFFSET),
                                     (column * WIDTH / 3 + WIDTH / 6, HEIGHT - OFFSET), 5)
                self.winner = self.board[0][column]
                return True

        # Check vertical locations for win
        for row in range(self.size[0]):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] != 0:
                # draw win line if not simulated
                if not self.simulated_board:
                    pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, row * HEIGHT / 3 + HEIGHT / 6),
                                     (WIDTH - OFFSET, row * HEIGHT / 3 + HEIGHT / 6), 5)
                    self.winner = int(self.board[row][0])
                return True

        # Check diagonal locations for win
        if self.board[2][0] == self.board[1][1] == self.board[0][2] and self.board[2][0] != 0:
            # draw win line if not simulated
            if not self.simulated_board:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, HEIGHT - OFFSET), (WIDTH - OFFSET, OFFSET), 5)
                self.winner = int(self.board[2][0])
            return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            # draw win line
            if not self.simulated_board:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), 5)
                self.winner = int(self.board[0][0])
            return True

        return False

    def reset_game(self):
        self.board = np.zeros((3, 3))
        self.game_over = False
        self.winner = None
        self.screen.fill(BG_COLOR)
        self.player_turn = 1
        draw_lines(self.screen)
        pygame.display.update()

    def get_valid_moves(self):
        return np.argwhere(self.board == 0)

    def change_turn(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1

    def new_game_menu(self, event: pygame.event.Event, font: pygame.font.Font):
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
    def __init__(self, player_num: int):
        self.player_num = player_num

    def draw_shapes(self, pos: tuple, screen: pygame.Surface):
        if self.player_num == 1:
            pygame.draw.circle(screen, LINE_COLOR, pos, 60, 15)
        else:
            pygame.draw.line(screen, LINE_COLOR, (pos[0] - 60, pos[1] - 60), (pos[0] + 60, pos[1] + 60), 15)
            pygame.draw.line(screen, LINE_COLOR, (pos[0] + 60, pos[1] - 60), (pos[0] - 60, pos[1] + 60), 15)
        return True

    def make_move(self, game: Game, screen: pygame.Surface):
        x, y = pygame.mouse.get_pos()
        column = int(x // (WIDTH / 3))
        row = int(y // (HEIGHT / 3))
        if game.available_square(row, column):
            game.mark_square(row, column, self.player_num)
            x_coord = (column * WIDTH / 3) + WIDTH / 6
            y_coord = (row * HEIGHT / 3) + HEIGHT / 6
            self.draw_shapes((x_coord, y_coord), screen)





class ComputerPlayer(Player):
    def __init__(self, player_num: int):
        super().__init__(player_num)

    def minimax(self, board: ndarray, game: Game, current_player: int, maximizing_player: bool):
        state = game.check_win()
        if state:
            if game.winner == current_player:
                return 1
            elif game.winner == 0:
                return 0
            else:
                return -1

        if maximizing_player:
            best_score = -math.inf
            for row, column in game.get_valid_moves():
                board[row][column] = current_player
                score = self.minimax(board, game, 1 if current_player == 2 else 2, False)
                board[row][column] = 0
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row, column in game.get_valid_moves():
                board[row][column] = current_player
                score = self.minimax(board, game, 1 if current_player == 2 else 2, True)
                board[row][column] = 0
                best_score = min(score, best_score)
            return best_score

    def find_optimal_move(self, board: ndarray, game: Game):
        """This code implements the minimax algorithm that drives the computer player. This should return an index
        for the best possible move"""
        game.simulated_board = True
        best_score = -math.inf
        best_move = None
        for row, column in game.get_valid_moves():
            board[row][column] = game.player_turn
            score = self.minimax(board, game, game.player_turn, False)
            board[row][column] = 0
            if score > best_score:
                best_score = score
                best_move = (row, column)
        game.simulated_board = False
        game.winner = None
        return best_move

    def make_move(self, game: Game, screen: pygame.Surface):
        """This will use the minimax algorithm to determine the best move for the computer player."""
        if not game.is_board_full():
            row, column = self.find_optimal_move(game.board, game)
            game.mark_square(row, column, self.player_num)
            x_coord = (column * WIDTH / 3) + WIDTH / 6
            y_coord = (row * HEIGHT / 3) + HEIGHT / 6
            self.draw_shapes((x_coord, y_coord), screen)
