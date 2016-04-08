import random
import mcts
import alpha_beta


def random_algo(board):
    return random.choice(list(board.get_legal_actions()))
    

def mcts_algo(board, time_limit):
    return mcts.uct(board, time_limit)

def alpha_beta_algo(board, time_limit):
    return alpha_beta.search(board, time_limit)
