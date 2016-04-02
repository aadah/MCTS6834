import game.py as game
import time as time
import random as random

Cp = 0
###########################################################
# monte carlo tree search algorithm using UCT heuristic
# Input: class Board represents the current game board
#        time limit of calculation in second
# Output: class Action represents the best action to take
##########################################################
def uct(board, time_budget):
    # record start time
    start_time = time.time()
    root = geme.Node(None, board, None)
    while (time.time() - start_time) < time_budget:
        tree_terminal = treepolicy(root)
        reward = randomsearch(tree_terminal.get_board())
        backup(tree_terminal, reward)
    return bestchild(root, 0).get_action()

###########################################################
# heuristically search to the leaf level
# Input: a node that want to search down
# Output: the leaf node that we expand till
##########################################################
def treepolicy(node):
    while not node.get_board().is_terminal():
        if not node.fully_expanded():
            return expand(node)
        else:
            node = bestchild(node, Cp)
    return node

###########################################################
# expand a node since it is not fully expanded
# Input: a node that want to be expanded
# Output: the child node
##########################################################
def expand(node):
    # get the current board
    board = node.get_board()
    
    # find unvisited actions in set
    visited_actions = set([child.get_action() for child in node.get_children()])
    all_actions = board.get_legal_actions()
    unvisited_actions = all_actions.difference(visited_actions)
    
    # random sample an action
    action = random.sample(unvisited_actions, 1)[0]
    
    new_board = action.apply(board)
    child = Node(action, new_board, node)
    node.children.append(child)
    return

###########################################################
# get the best child from this node (using heuristic)
# Input: a node, which we want to find the best child of
#        Cp, a searching constant
# Output: the child node
###########################################################
def bestchild(node, c):
    all_children = node.get_children()
    heuristics = [child.value(c) for child in all_children]
    max_index = heuristics.index(max(heuristics))
    return all_children[max_index]

###########################################################
# randomly picking moves to reach the end game
# Input: a board that want to start randomly picking moves
# Output: the reward when the game terminates
###########################################################
def randomsearch(board)
    raise NotImplemented

###########################################################
# reward update for the tree after one simulation
# Input: a node that we want to backup from
#        reward value
# Output: nothing
###########################################################
def backup(node, reward):
    while node is not None:
        visit(node)
        node.q_value += reward
        node = node.get_parent()
    return

