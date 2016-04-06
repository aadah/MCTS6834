import game
import random

from pprint import pprint

# just some hacky tests

def test_0():
    s = [['B', 'R', 'B', 'B', 'B', 'R'],
         ['B', 'B', 'R', 'B', 'R', 'B'],
         ['B', 'B', 'B', 'R', 'R', 'B'],
         ['R', 'R', 'B', 'B', 'R', 'B'],
         ['R', 'R', 'B', 'R', 'B', 'R'],
         ['B', 'B', 'R', 'R', 'B', 'R'],
         ['R', 'B', 'R', 'B', 'R', '-']]
    board = game.ConnectFourBoard(s, 'B')
    board.last_move = (0,0)
    print board.is_terminal()
    
def test_1():
    board = game.ConnectFourBoard()
    while not board.is_terminal():
        actions = board.get_legal_actions()
        action = random.choice(list(actions))
        board = action.apply(board)
        pprint(board.state)
    print board.is_terminal()
    print board.last_move

def test_2():
    board = game.ConnectFourBoard()
    me = game.ConnectFourHumanPlayer('foo')
    while not board.is_terminal():
        pprint(board.state)
        action = me.choose_action(board)
        board = action.apply(board)
    print board.is_terminal()
    print board.last_move

def test_3():
    board = game.ConnectFourBoard()
    node = game.Node(board)
    actions = board.get_legal_actions()

    while not node.is_fully_expanded():
        action = random.choice(list(actions))
        child = game.Node(action.apply(board), action, node)
        node.add_child(child)

    print len(actions) == 0 # should be True

def test_4():
    board = game.ConnectFourBoard()
    node = game.Node(board)

    while not node.board.is_terminal():
        actions = node.board.get_legal_actions()
        action = random.choice(list(actions))
        child = game.Node(action.apply(node.board), action, node)
        node.add_child(child)
        node = child

    pprint(node.board.state)
    print node.board.last_move

def random_algo(board):
    return random.choice(list(board.get_legal_actions()))

def test_5():
    board = game.ConnectFourBoard()
    player_1 = game.ComputerPlayer('one', random_algo)
    player_2 = game.ComputerPlayer('two', random_algo)
    sim = game.Simulation(board, player_1, player_2)
    sim.run()
    pprint(sim.board.state)
    print 'Last move: {}'.format(sim.board.last_move)
    print 'Rewards: {}'.format(sim.board.reward_vector())

#test_0()
#test_1()
#test_2()
#test_3()
#test_4()
test_2()
