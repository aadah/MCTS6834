import mcts as mcts
import algo
import random as random
import game as game
from pprint import pprint
import re

#TODO: test_9 failed, can't handle a completely filled board

# the game playing
def test_0():
    # human decide color
    print 'red first, do you want to play in black (type B), or red (type R)?'
    human_color = raw_input("B/R ")
    
    # human decide difficulty
    print 'how many seconds do you want computer to think? (5 seconds recommended)'
    computer_time = int(raw_input("computer thinking time: "))
    
    # create player
    if human_color == 'R':
        computer_color = 'B'
    else:
        computer_color = 'R'
    board = game.ConnectFourBoard()
    human = game.ConnectFourHumanPlayer('foo')
    
    if human_color == 'R':
        while not board.is_terminal():
            pprint(board.state)
            action = human.choose_action(board)
            board = action.apply(board)
            if board.is_terminal():
                break
            pprint(board.state)
            action = mcts.uct(board, computer_time)
            board = action.apply(board)
    if human_color == 'B':
        while not board.is_terminal():
            pprint(board.state)
            action = mcts.uct(board, computer_time)
            board = action.apply(board) 
            if board.is_terminal():
                break
            pprint(board.state) 
            action = human.choose_action(board)
            board = action.apply(board)  
    
    # game ends, tell who wins
    pprint(board.state)
    col, row = board.last_move
    winning_color = board.state[col][row]
    if human_color == winning_color:
        print 'you win!'
    else:
        print 'you lose!'
    
    
# test of expand function
# should print out all of the possible next step
def test_1():
    s = [['-', '-', '-', '-', '-', '-'],
         ['R', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['B', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-']]
    board = game.ConnectFourBoard(s, 'B')
    node = game.Node(board)
    pprint(node.get_board().state)
    for i in range(7):
        mcts.expand(node)
    count = 0
    for child in node.get_children():
        count += 1
        print "child", count
        pprint(child.get_board().state)
    return

# test of randomsearch function
# should print out a random search result
# to check the searching progress, decomment the code in mcts.py
def test_2():
    s = [['-', '-', '-', '-', '-', '-'],
         ['R', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['B', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.randomsearch(board, 'B')
    return

# test of blocking opponent
# should have high possibility return "ConnectFourAction(color=B,col=1,row=3)"
def test_3():
    s = [['B', '-', '-', '-', '-', '-'],
         ['R', 'R', 'R', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['B', 'B', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0)

# test of winning move
# should have high possibility return "ConnectFourAction(color=B,col=3,row=3)"
def test_4():
    s = [['-', '-', '-', '-', '-', '-'],
         ['R', 'R', 'R', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['B', 'B', 'B', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0)

# test of edge case (empty board)
def test_5():
    s = [['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0)  
    
# test of almost complete the board with a tie
def test_6():
    s = [['R', 'B', 'B', 'R', 'R', '-'],
         ['B', 'B', 'R', 'R', 'B', '-'],
         ['B', 'R', 'B', 'B', 'R', '-'],
         ['B', 'R', 'R', 'B', 'R', '-'],
         ['R', 'R', 'R', 'B', 'R', '-'],
         ['B', 'B', 'R', 'R', 'B', '-'],
         ['B', 'R', 'B', 'R', 'B', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0)  

# test of last move with a tie
# should always return "ConnectFourAction(color=B,col=6,row=5)"
def test_7():
    s = [['R', 'B', 'B', 'R', 'R', 'R'],
         ['B', 'B', 'R', 'R', 'B', 'B'],
         ['B', 'R', 'B', 'B', 'R', 'R'],
         ['B', 'R', 'R', 'B', 'R', 'B'],
         ['R', 'R', 'R', 'B', 'R', 'B'],
         ['B', 'B', 'R', 'R', 'B', 'R'],
         ['B', 'R', 'B', 'R', 'B', '-']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0) 

# test of an always lose board
def test_8():
    s = [['R', 'B', 'B', 'R', 'R', 'B'],
         ['B', 'B', 'R', 'R', 'B', '-'],
         ['B', 'R', 'B', 'B', 'R', 'R'],
         ['B', 'R', 'R', 'B', 'R', 'R'],
         ['R', 'R', 'R', 'B', 'R', 'R'],
         ['B', 'B', 'R', 'R', 'B', '-'],
         ['B', 'R', 'B', 'R', 'B', 'B']]
    board = game.ConnectFourBoard(s, 'B')
    print mcts.uct(board, 1.0) 
    
# test of a complete board
def test_9():
    s = [['R', 'B', 'B', 'R', 'R', 'R'],
         ['B', 'B', 'R', 'R', 'B', 'B'],
         ['B', 'R', 'B', 'B', 'R', 'R'],
         ['B', 'R', 'R', 'B', 'R', 'B'],
         ['R', 'R', 'R', 'B', 'R', 'B'],
         ['B', 'B', 'R', 'R', 'B', 'R'],
         ['B', 'R', 'B', 'R', 'B', 'B']]
    board = game.ConnectFourBoard(s, 'R')
    print mcts.uct(board, 1.0) 

    
def test_10():
    # human decide color
    print "Which color (red or black) do you want to play? Red goes first."
    human_color = raw_input("Enter 'R' or 'B': ").strip()
    
    # human decide difficulty
    print 'How many seconds will you allow your computer opponent to think? Enter a number (5 is recommended).'
    time_limt = float(raw_input("computer thinking time: ").strip())

    board = game.ConnectFourBoard()
    human = game.ConnectFourHumanPlayer('human')
    computer = game.ComputerPlayer('computer', algo.mcts_algo, time_limt)
    
    if human_color == game.ConnectFourBoard.RED:
        sim = game.Simulation(board, human, computer)
    else:
        sim = game.Simulation(board, computer, human)

    sim.run(visualize=True)

    
test_3()
