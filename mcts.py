import game as game
import time as time
import random as random
from pprint import pprint
import re

Cp = 5
###########################################################
# monte carlo tree search algorithm using UCT heuristic
# Input: class Board represents the current game board
#        time limit of calculation in second
# Output: class Action represents the best action to take
##########################################################
def uct(board, time_budget):
    # record start time
    start_time = time.time()
    root = game.Node(board, None, None)
    
    ########### debug part: print the root board ###########
    # print 'root game board:'
    # pprint(root.get_board().state)
    
    computer_color = board.turn
    while (time.time() - start_time) < time_budget:
        tree_terminal = treepolicy(root)
        reward = randomsearch(tree_terminal.get_board(), computer_color)
        backup(tree_terminal, reward)
        
        ######### debug part: step by step debugging#########
        # display(root)
        # start_time = time.time()
        
    return bestchild(root, 0).get_action()

###########################################################
# heuristically search to the leaf level
# Input: a node that want to search down
# Output: the leaf node that we expand till
##########################################################
def treepolicy(node):
    while not node.get_board().is_terminal():
        if not node.is_fully_expanded():
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
    
    visited_actions = set([child.get_action() for child in node.get_children()])
    all_actions = board.get_legal_actions()
    
    # get the unvisited_actions by getting difference of all_actions and visited actions
    unvisited_actions = set([])
    for all_action in all_actions:
        not_visited = True
        for visited_action in visited_actions:
            if hash(visited_action) == hash(all_action):
                not_visited = False
        if not_visited:
            unvisited_actions.add(all_action)
    
    # random sample an action
    action = random.choice(list(unvisited_actions))
    
    new_board = action.apply(board)
    child = game.Node(new_board, action, node)
    node.children.append(child)
    return child

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
#        the color of computer (black or red)
# Output: the reward when the game terminates
###########################################################
def randomsearch(board, computer_color):
    
    ####### debug part: print out the board request for random search ##########
    # print 'random search requested board:'
    # pprint(board.state)
    
    while not board.is_terminal():
        actions = board.get_legal_actions()
        action = random.choice(list(actions))
        board = action.apply(board)
    # (R,B)
    reward_vector = board.reward_vector()
    if computer_color == 'R':
        reward = reward_vector[0]
    else:
        reward = reward_vector[1]
        
    ######## debug part: print out random search result #########
    # print 'random search end board:'
    # pprint(board.state)
    # print 'computer color:', computer_color, ',reward:', reward
    
    return reward

###########################################################
# reward update for the tree after one simulation
# Input: a node that we want to backup from
#        reward value
# Output: nothing
###########################################################
def backup(node, reward):
    while node is not None:
        node.visit()
        node.q = node.q + reward
        node = node.get_parent()
    return

###########################################################
# debug part: print out the nodes of tree
# Input: a root node
# Output: nothing (just printing)
###########################################################
def display(node):
    pprint(treemap(node))
    INPUT_RE = re.compile(r'\s*(\d+)\s*')
    inp = raw_input("#################press any button to run next step#################")
    m = INPUT_RE.match(inp)

def treemap(node):
    if node.get_children():
        tree = ['middlenode:', (node.get_board().state, node.num_visits, node.q)]
        for child in node.get_children():
            tree.append(treemap(child))
        return tree
    else:
        return ['leafnode:', (node.get_board().state, node.num_visits, node.q)]
    