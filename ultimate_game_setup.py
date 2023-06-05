"""This code creates the player and computer player classes, as well as the game settings and functions.
This code is import only. The logic is handled in the main file."""

import numpy as np
import pygame
from numpy import ndarray
import math

WIDTH, HEIGHT = 900, 900
BG_COLOR = (220, 220, 220)
LINE_COLOR = (0, 0, 0)
BOARD_SIZE = (3, 3)
OFFSET = 40
delay = 0.5


def draw_lines(screen: pygame.Surface):
    """This draws the main tic-tac-toe board lines."""
    local_board_x_offset = WIDTH / 9
    local_board_y_offset = HEIGHT / 9

    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3, OFFSET), (WIDTH / 3, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3, OFFSET), (2 * WIDTH / 3, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT / 3), (WIDTH - OFFSET, HEIGHT / 3), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, 2 * HEIGHT / 3), (WIDTH - OFFSET, 2 * HEIGHT / 3), 5)
    # After the global board is drawn, smaller local boards are drawn inside each grid space.

    # top left box
    pygame.draw.line(screen, LINE_COLOR, (local_board_x_offset, local_board_y_offset - OFFSET),
                     (local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 - local_board_x_offset, local_board_y_offset - OFFSET),
                     (WIDTH / 3 - local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, local_board_y_offset + OFFSET / 2),
                     (WIDTH / 3 - OFFSET, local_board_y_offset + OFFSET / 2), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT / 3 - local_board_y_offset),
                     (WIDTH / 3 - OFFSET, HEIGHT / 3 - local_board_y_offset), 5)

    # top middle box
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + local_board_x_offset, local_board_y_offset - OFFSET),
                     (WIDTH / 3 + local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 - local_board_x_offset, local_board_y_offset - OFFSET),
                     (2 * WIDTH / 3 - local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, local_board_y_offset + OFFSET / 2),
                     (2 * WIDTH / 3 - OFFSET, local_board_y_offset + OFFSET / 2), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, HEIGHT / 3 - local_board_y_offset),
                     (2 * WIDTH / 3 - OFFSET, HEIGHT / 3 - local_board_y_offset), 5)

    # top right box
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + local_board_x_offset, local_board_y_offset - OFFSET),
                     (2 * WIDTH / 3 + local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - local_board_x_offset, local_board_y_offset - OFFSET),
                     (WIDTH - local_board_x_offset, HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, local_board_y_offset + OFFSET / 2),
                     (WIDTH - OFFSET, local_board_y_offset + OFFSET / 2), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, HEIGHT / 3 - local_board_y_offset),
                     (WIDTH - OFFSET, HEIGHT / 3 - local_board_y_offset), 5)

    # middle left box
    pygame.draw.line(screen, LINE_COLOR, (local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 - local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (WIDTH / 3 - local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT / 3 + local_board_y_offset),
                     (WIDTH / 3 - OFFSET, HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, 2 * HEIGHT / 3 - local_board_y_offset),
                     (WIDTH / 3 - OFFSET, 2 * HEIGHT / 3 - local_board_y_offset), 5)

    # middle middle box
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (WIDTH / 3 + local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 - local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (2 * WIDTH / 3 - local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, HEIGHT / 3 + local_board_y_offset),
                     (2 * WIDTH / 3 - OFFSET, HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, 2 * HEIGHT / 3 - local_board_y_offset),
                     (2 * WIDTH / 3 - OFFSET, 2 * HEIGHT / 3 - local_board_y_offset), 5)

    # middle right box
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (2 * WIDTH / 3 + local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - local_board_x_offset, HEIGHT / 3 + OFFSET),
                     (WIDTH - local_board_x_offset, 2 * HEIGHT / 3 - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, HEIGHT / 3 + local_board_y_offset),
                     (WIDTH - OFFSET, HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, 2 * HEIGHT / 3 - local_board_y_offset),
                     (WIDTH - OFFSET, 2 * HEIGHT / 3 - local_board_y_offset), 5)

    # bottom left box
    pygame.draw.line(screen, LINE_COLOR, (local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 - local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (WIDTH / 3 - local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, 2 * HEIGHT / 3 + local_board_y_offset),
                     (WIDTH / 3 - OFFSET, 2 * HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (OFFSET, HEIGHT - local_board_y_offset),
                     (WIDTH / 3 - OFFSET, HEIGHT - local_board_y_offset), 5)

    # bottom middle box
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (WIDTH / 3 + local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 - local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (2 * WIDTH / 3 - local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, 2 * HEIGHT / 3 + local_board_y_offset),
                     (2 * WIDTH / 3 - OFFSET, 2 * HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH / 3 + OFFSET, HEIGHT - local_board_y_offset),
                     (2 * WIDTH / 3 - OFFSET, HEIGHT - local_board_y_offset), 5)

    # bottom right box
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (2 * WIDTH / 3 + local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - local_board_x_offset, 2 * HEIGHT / 3 + OFFSET),
                     (WIDTH - local_board_x_offset, HEIGHT - OFFSET), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, 2 * HEIGHT / 3 + local_board_y_offset),
                     (WIDTH - OFFSET, 2 * HEIGHT / 3 + local_board_y_offset), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH / 3 + OFFSET, HEIGHT - local_board_y_offset),
                     (WIDTH - OFFSET, HEIGHT - local_board_y_offset), 5)


def start_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Tic-Tac-Toe")
    screen.fill(BG_COLOR)
    return screen


class Game:
    global_board: ndarray
    local_boards: ndarray

    def __init__(self, screen: pygame.Surface, graphics_enabled: bool):
        self.global_board = np.zeros((3, 3))
        self.local_boards = np.zeros((3, 3, 3, 3))
        self.size = BOARD_SIZE
        self.game_over = False
        self.winner = None
        self.new_game = True
        self.single_player = False
        self.multi_player = False
        self.aigame = False
        self.screen = screen
        self.player_turn = 1
        self.choose_turn = True
        self.graphics_enabled = graphics_enabled

    def mark_local_square(self, local_board_coord, row_num: int, column: int, player_num: int):
        self.local_boards[local_board_coord[0], local_board_coord[1], row_num, column] = player_num

    def unmark_local_square(self, local_board_coord, row_num: int, column: int):
        self.local_boards[local_board_coord[0], local_board_coord[1], row_num, column] = 0

    def mark_global_square(self, row_num: int, column: int, player_num: int):
        self.global_board[row_num][column] = player_num

    def unmark_global_square(self, row_num: int, column: int):
        self.global_board[row_num][column] = 0

    def available_local_square(self, local_board_coord, row_num: int, column: int):
        print(self.local_boards[local_board_coord[0], local_board_coord[1], row_num, column] == 0)
        return self.local_boards[local_board_coord[0], local_board_coord[1], row_num, column] == 0

    def available_global_square(self, row_num: int, column: int):
        return self.global_board[row_num][column] == 0

    def is_local_board_full(self, local_board_coord):
        return not np.any(self.local_boards[local_board_coord[0], local_board_coord[1]] == 0)

    def is_global_board_full(self):
        return not np.any(self.global_board == 0)

    def change_turn(self):
        self.player_turn = 3 - self.player_turn

    def check_global_win(self):
        # Check horizontal locations for win
        for column in range(self.size[1]):
            if self.global_board[0][column] == self.global_board[1][column] == self.global_board[2][column] and \
                    self.global_board[0][column] != 0:
                # draw win line if not simulated
                if self.graphics_enabled:
                    pygame.draw.line(self.screen, LINE_COLOR, (column * WIDTH / 3 + WIDTH / 6, OFFSET),
                                     (column * WIDTH / 3 + WIDTH / 6, HEIGHT - OFFSET), 5)
                self.winner = self.global_board[0][column]
                return True

        # Check vertical locations for win
        for row in range(self.size[0]):
            if self.global_board[row][0] == self.global_board[row][1] == self.global_board[row][2] and \
                    self.global_board[row][0] != 0:
                # draw win line if not simulated
                if self.graphics_enabled:
                    pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, row * HEIGHT / 3 + HEIGHT / 6),
                                     (WIDTH - OFFSET, row * HEIGHT / 3 + HEIGHT / 6), 5)
                self.winner = int(self.global_board[row][0])
                return True

        # Check diagonal locations for win
        if self.global_board[2][0] == self.global_board[1][1] == self.global_board[0][2] and self.global_board[2][
                0] != 0:
            # draw win line if not simulated
            if self.graphics_enabled:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, HEIGHT - OFFSET), (WIDTH - OFFSET, OFFSET), 5)
            self.winner = int(self.global_board[2][0])
            return True
        if self.global_board[0][0] == self.global_board[1][1] == self.global_board[2][2] and self.global_board[0][
                0] != 0:
            # draw win line
            if self.graphics_enabled:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), 5)
            self.winner = int(self.global_board[0][0])
            return True

        return False

    def check_local_win(self, local_board_coord):
        # Check horizontal locations for win
        for column in range(self.size[1]):
            if self.local_boards[local_board_coord][0][column] == self.local_boards[local_board_coord][1][column] == \
                    self.local_boards[local_board_coord][2][column] and self.local_boards[local_board_coord][0][
                    column] != 0:
                # draw win line if not simulated
                if self.graphics_enabled:
                    pygame.draw.line(self.screen, LINE_COLOR, (column * WIDTH / 3 + WIDTH / 6, OFFSET),
                                     (column * WIDTH / 3 + WIDTH / 6, HEIGHT - OFFSET), 5)
                self.winner = self.local_boards[local_board_coord][0][column]
                return True

        # Check vertical locations for win
        for row in range(self.size[0]):
            if self.local_boards[local_board_coord][row][0] == self.local_boards[local_board_coord][row][1] == \
                    self.local_boards[local_board_coord][row][2] and self.local_boards[local_board_coord][row][0] != 0:
                # draw win line if not simulated
                if self.graphics_enabled:
                    pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, row * HEIGHT / 3 + HEIGHT / 6),
                                     (WIDTH - OFFSET, row * HEIGHT / 3 + HEIGHT / 6), 5)
                self.winner = int(self.local_boards[local_board_coord][row][0])
                return True

        # Check diagonal locations for win
        if self.local_boards[local_board_coord][2][0] == self.local_boards[local_board_coord][1][1] == \
                self.local_boards[local_board_coord][0][2] and self.local_boards[local_board_coord][2][0] != 0:
            # draw win line if not simulated
            if self.graphics_enabled:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, HEIGHT - OFFSET), (WIDTH - OFFSET, OFFSET), 5)
            self.winner = int(self.local_boards[local_board_coord][2][0])
            return True
        if self.local_boards[local_board_coord][0][0] == self.local_boards[local_board_coord][1][1] == \
                self.local_boards[local_board_coord][2][2] and self.local_boards[local_board_coord][0][0] != 0:
            # draw win line
            if self.graphics_enabled:
                pygame.draw.line(self.screen, LINE_COLOR, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), 5)
            self.winner = int(self.local_boards[local_board_coord][0][0])
            return True

        return False

    def reset_game(self):
        self.global_board = np.zeros((3, 3))
        self.local_boards = np.zeros((3, 3, 3, 3))
        self.game_over = False
        self.winner = None
        self.player_turn = 1
        if self.graphics_enabled:
            self.screen.fill(BG_COLOR)
            draw_lines(self.screen)
            pygame.display.update()

    def get_valid_local_moves(self, local_board_coord: ndarray):
        return np.argwhere(self.local_boards[local_board_coord[0], local_board_coord[1]] == 0)

    def new_game_menu(self, event: pygame.event.Event, font: pygame.font.Font):
        if self.new_game:
            if self.graphics_enabled:
                self.screen.fill(BG_COLOR)
                text = font.render("Press 1 for single player, press 2 for multiplayer.", True, LINE_COLOR)
                self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.single_player = True
                        self.multi_player = False
                        self.aigame = False
                        self.new_game = False
                        self.reset_game()
                    elif event.key == pygame.K_2:
                        self.multi_player = True
                        self.single_player = False
                        self.aigame = False
                        self.new_game = False
                        self.reset_game()
                    elif event.key == pygame.K_3:
                        self.aigame = True
                        self.single_player = False
                        self.multi_player = False
                        self.new_game = False
                        self.reset_game()

    def choose_turn_menu(self, event, font: pygame.font.Font):
        """This lets the player choose whether they or the computer go first."""
        if self.choose_turn:
            self.screen.fill(BG_COLOR)
            text = font.render("Press 1 to go first, press 2 to let the computer go first.", True, LINE_COLOR)
            self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player_turn = 1
                    self.reset_game()
                    self.choose_turn = False
                    return True
                elif event.key == pygame.K_2:
                    self.player_turn = 2
                    self.reset_game()
                    self.choose_turn = False
                    return True


class Player:
    def __init__(self, player_num: int):
        self.player_num = player_num

    def draw_local_shapes(self, pos: tuple, screen: pygame.Surface):
        size = 20
        width = 5
        if self.player_num == 1:
            pygame.draw.circle(screen, LINE_COLOR, pos, size, width)
        else:
            pygame.draw.line(screen, LINE_COLOR, (pos[0] - size, pos[1] - size), (pos[0] + size, pos[1] + size), width)
            pygame.draw.line(screen, LINE_COLOR, (pos[0] + size, pos[1] - size), (pos[0] - size, pos[1] + size), width)
        return True

    def make_move(self, game: Game, screen: pygame.Surface, local_board_coord):
        """This function is called when the player makes a move. It should only allow the player to make a move in the
        provided local board."""
        # This first finds the local board that is being played in.
        global_x, global_y = pygame.mouse.get_pos()
        column = int(global_x // (WIDTH / 3))
        row = int(global_y // (HEIGHT / 3))
        local_board_coord = local_board_coord
        # check if the selected local board is the same as the provided local board
        if local_board_coord != [row, column]:
            return False
        
        # This then finds the local square that is being played in.
        local_x = global_x % (WIDTH / 3)
        local_y = global_y % (HEIGHT / 3)
        local_column = int(local_x // (WIDTH / 9))
        local_row = int(local_y // (HEIGHT / 9))
        print(local_board_coord, local_row, local_column)
        if game.available_local_square(local_board_coord, local_row, local_column):
            game.mark_local_square(local_board_coord, local_row, local_column, self.player_num)
            # find local square coordinates
            x_coord = int((column * (WIDTH / 3)) + (local_column * (WIDTH / 9)) + (WIDTH / 18))
            y_coord = int((row * (HEIGHT / 3)) + (local_row * (HEIGHT / 9)) + (HEIGHT / 18))
            if game.graphics_enabled:
                self.draw_local_shapes((x_coord, y_coord), screen)
            game.change_turn()
        return [local_row, local_column]


class ComputerPlayer(Player):
    def __init__(self, player_num: int):
        super().__init__(player_num)

    def make_move(self, game: Game, screen: pygame.Surface):
        """This will randomly pick a move."""
        pass
