"""This code uses tabular q learning to train a tic-tac-toe agent."""

import game_setup as setup
import numpy as np
import matplotlib.pyplot as plt


def convert_to_grid(pos):
    # convert the position (0-8) to a grid position (row, col)
    row = pos // 3
    col = pos % 3
    return row, col


class QTable:
    def __init__(self):
        self.q_table = np.zeros([3 ** 9, 9])
        self.state_key_vector = 3 ** np.arange(9)

    def state_to_key(self, state):
        # convert the state to a unique key
        return np.dot(state.flatten(), self.state_key_vector)

    def __call__(self, state):
        # return the q values for the given state, by converting the state to a unique key
        return self.q_table[int(self.state_to_key(state))]

    def save(self, filename):
        if not filename.endswith(".csv"):
            filename = filename + ".csv"
        np.savetxt(filename, self.q_table, delimiter=",")

    def load(self, filename):
        if not filename.endswith(".csv"):
            filename = filename + ".csv"
        self.q_table = np.loadtxt(filename, delimiter=",")


class QAgent:
    def __init__(self, game, player_num, q_table: QTable = None, epsilon=0.1, alpha=0.1, gamma=0.95):
        self.game = game
        self.player_num = player_num
        self.opp_num = 3 - player_num
        self.q_table = QTable() if q_table is None else q_table
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def best_action(self, state):
        """ get the best action for the given state """
        return np.argmax(self.q_table(state)) if self.game.player_turn == self.player_num else \
            np.argmin(self.q_table(state))

    def make_move(self):
        """ make a move for the agent by using an epsilon greedy policy """
        state = self.game.board
        if np.random.random() < self.epsilon:
            action = int(np.random.randint(0, 9, 1))
        else:
            action = self.best_action(state)
        return action

    def learn(self, state, action, next_state, reward):
        """ learn from the previous move """
        # if game finished then set the q value to the reward
        if self.game.game_over or self.game.is_board_full():
            expected_q = reward
        else:
            # otherwise update the q value using the bellman equation
            expected_q = reward + self.gamma * np.max(self.q_table(next_state))
        # update the q table
        q_values = self.q_table(state)
        q_values[action] += self.alpha * (expected_q - q_values[action])


reward_list = []


def play_training_game(agent1, agent2, game):
    """ play a game between two agents. The agents should be trained to not make invalid moves """
    # reset the game
    game.reset_game()
    # create reward list to plot later
    reward_sum = 0
    # loop until the game is over
    while not game.check_win() and not game.is_board_full():
        # get the current state

        state = game.board
        invalid_move = False
        # get the current player's turn
        player = game.player_turn
        # get the action for the current player
        action = agent1.make_move() if player == agent1.player_num else agent2.make_move()
        # make the move
        # heavily penalize the agent if the move is invalid

        move = convert_to_grid(action)
        if not game.available_square(move[0], move[1]):
            invalid_move = True

        game.mark_square(move[0], move[1], player)
        # get the next state
        next_state = game.board
        # get the reward for the current player
        reward = game.evaluate(player, 3 - player)
        # learn from the previous move if it was not invalid, otherwise penalize the agent
        if not invalid_move:
            agent1.learn(state, action, next_state, reward) if player == agent1.player_num else \
                agent2.learn(state, action, next_state, reward)
        else:
            agent1.learn(state, action, next_state, -10) if player == agent1.player_num else \
                agent2.learn(state, action, next_state, -10)
        game.change_turn()
        # add the reward to the reward list
        reward_sum += reward
    reward_list.append(reward_sum)


def main():
    game = setup.Game(setup.start_game(), False)
    qtable = QTable()
    agent1 = QAgent(game, 1, epsilon=0.5, alpha=0.01, gamma=0.9, q_table=qtable)
    agent2 = QAgent(game, 2, epsilon=0.5, alpha=0.01, gamma=0.9, q_table=qtable)
    #agent2 = setup.ComputerPlayer(2, True)
    # play 10000 games
    num_episodes = 100000
    for i in range(num_episodes):
        play_training_game(agent1, agent2, game)
        # print the progress
        if i % 1000 == 0:
            print(f"Game: {i} out of {num_episodes}")

    # save the q table
    qtable.save("qtable.csv")

    # plot the reward list
    # chunk the reward list into 1000 chunks
    chunked_reward_list = [reward_list[i:i + 1000] for i in range(0, len(reward_list), 1000)]
    # get the average reward for each chunk
    avg_reward_list = [sum(chunk) / len(chunk) for chunk in chunked_reward_list]
    # plot the average reward list
    plt.plot(avg_reward_list)
    plt.xlabel("1000s of games")
    plt.ylabel("Average reward")
    plt.show()



if __name__ == "__main__":
    main()
