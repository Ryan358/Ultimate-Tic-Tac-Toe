"""This file will create a dataset for training a neural network to play tic-tac-toe. The dataset will be a list of
tuples, where each tuple contains a board state and the corresponding move to make. The board state will be a 3x3 array
with either 0, 1, or 2. 0 represents an empty space, 1 represents a space occupied by player
1, and 2 represents a space occupied by player 2. The move will be a numpy array with the row and column of the chosen
square."""

import game_setup as setup
import numpy as np
import pickle

dataset = []
player1 = setup.ComputerPlayer(1, True)
player2 = setup.ComputerPlayer(2, True)
game = setup.Game(graphics_enabled=False)


def play_regular_game(agent1, agent2, game):
    game_states = []
    game_actions = []
    rewards = []

    game_states.append(np.copy(game.board))
    action = agent1.make_move(game, None)
    game.change_turn()
    game_actions.append(action)

    while not game.check_win() and not game.is_local_board_full():
        game_states.append(np.copy(game.board))
        if game.player_turn == 1:
            action = agent1.make_move(game, None)
        else:
            action = agent2.make_move(game, None)
        # print(game.board)

        game_actions.append(action)
        game.change_turn()

    game.reset_game()
    # assign rewards to each player based on their moves
    if game.winner == 1:
        reward1 = 1
        reward2 = -1
    elif game.winner == 2:
        reward1 = -1
        reward2 = 1
    else:
        reward1 = 0
        reward2 = 0

    # append rewards to their own list
    # Store the transition in the training dataset
    for i in range(len(game_states)-1):
        dataset.append((game_states[i], game_actions[i], reward1, game_states[i + 1]))


def create_data(num_games):
    for i in range(num_games):
        play_regular_game(player1, player2, game)
        game.reset_game()
    with open('tic_tac_toe_dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)


create_data(1)

data = pickle.load(open('tic_tac_toe_dataset.pkl', 'rb'))
print(data)
