import copy
import game
import time

def search(board, time_budget):
    # Initial queue of actions to investigate
    # (board, move to take if you want to see this board)
    # Really bad because making it better will need recursion and a heuristic
    deadline = time.time() + time_budget

    chosen_action = None
    for depth in range(12,24,2):
        _, new_chosen_action = alpha_beta(copy.copy(board), depth, -9001 * 9001, 9001 * 9001, True, deadline)
        if new_chosen_action:
            chosen_action = new_chosen_action
    return chosen_action

def heuristic(board):
    # board.state blah blah
    try:
        return board.reward_vector()[0]
    except:
        return 0

# Time to steal from wikipedia
# From https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
def alpha_beta(board, depth, alpha, beta, is_player, deadline):
    actions = board.get_legal_actions()
    if depth == 0 or len(actions) == 0 or time.time() > deadline:
        return (heuristic(board), None)
    if is_player:
        best_result = (-9001 * 9001, None)
        for action in actions:
            new_board = action.apply(board)
            (new_value, _) = alpha_beta(new_board, depth - 1, alpha, beta, False, deadline)

            if new_value > best_result[0]:
                best_result = (new_value, action)
            alpha = max(alpha, new_value)
            if beta <= alpha:
                break
        return best_result
    else:
        worst_result = (9001 * 9001, None)
        for action in actions:
            new_board = action.apply(board)
            new_value = alpha_beta(new_board, depth - 1, alpha, beta, True, deadline)
            if new_value < worst_result[0]:
                worst_result = (new_value, action)
            beta = min(beta, new_value)
            if beta <= alpha:
                break
        return worst_result
