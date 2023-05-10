"""A simple tic-tac-toe game in pygame. Contains both single player and multiplayer modes."""
import pygame
import sys
import game_setup as setup

screen = setup.start_game()

# create game object and potential player objects
game = setup.Game(screen, True)
player1 = setup.Player(1)
player2 = setup.Player(2)

# create the potential computer players. If single player is selected, the computer player will be player 2. There
# is an optional difficulty setting that ranges from 0-100 (default is 100).
com_player1 = setup.ComputerPlayer(1)
com_player2 = setup.ComputerPlayer(2)

sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(sysfont, setup.OFFSET)

while True:
    for event in pygame.event.get():
        # check if the game is in new game mode, if so, display the new game menu
        game.new_game_menu(event, font)
        if game.check_win():
            # if check_win returns true, end the game and print out the winner
            text = font.render(f"Player {int(game.winner)} wins!", True, setup.LINE_COLOR)
            screen.blit(text, (setup.WIDTH / 2 - text.get_width() / 2, text.get_height() / 2))
            game.game_over = True
        if game.is_board_full():
            # check if the game board is full, i.e. a draw
            game.game_over = True
        if event.type == pygame.QUIT:
            sys.exit()
        if game.multi_player:
            # alternate between player 1 and player 2, since we are in single player mode
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.new_game:
                if game.player_turn == 1:
                    player1.make_move(game, screen)
                    game.change_turn()
                else:
                    player2.make_move(game, screen)
                    game.change_turn()

        if game.single_player:
            # use computer player to make move as player 2
            moves = len(game.get_valid_moves())
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and not game.new_game:
                player1.make_move(game, screen)
                available_spaces = len(game.get_valid_moves())
                if available_spaces < moves and not game.check_win():
                    com_player2.make_move(game, screen)

        if game.aigame:
            moves = len(game.get_valid_moves())
            if not game.game_over and not game.new_game:
                com_player1.make_move(game, screen)
                available_spaces = len(game.get_valid_moves())
                if available_spaces < moves and not game.check_win():
                    com_player2.make_move(game, screen)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.new_game = True
                game.reset_game()

        if game.game_over:
            restart_text = font.render("Press R to restart", True, setup.LINE_COLOR)
            screen.blit(restart_text, (setup.WIDTH / 3 - restart_text.get_width(), setup.HEIGHT
                                       - restart_text.get_height()))
            quit_text = font.render("Press SPACE to quit", True, setup.LINE_COLOR)
            screen.blit(quit_text, (setup.WIDTH - quit_text.get_width(), setup.HEIGHT - quit_text.get_height()))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit("Thanks for playing!")

    pygame.display.update()
