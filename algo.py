import random

import mcts


def random_algo(board):
    return random.choice(list(board.get_legal_actions()))
    

def mcts_algo(board, time_limit):
    return mcts.uct(board, time_limit)
