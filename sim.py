import game
import algo

from pprint import pprint

def simulation():
    time_limit_1 = 0.01
    time_limit_2 = 0.1

    board = game.ConnectFourBoard()
    player_1 = game.ComputerPlayer('random', algo.mcts_algo, time_limit_1)
    player_2 = game.ComputerPlayer('mcts', algo.mcts_algo, time_limit_2)
    sim = game.Simulation(board, player_1, player_2)
    sim.run(visualize=False)
    pprint(sim.board.state)
    print 'Last move: {}'.format(sim.board.last_move)
    print 'Rewards: {}'.format(sim.board.reward_vector())
    

simulation()
