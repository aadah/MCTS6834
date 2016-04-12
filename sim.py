import game
import algo
import time

from IPython.display import display, display_html, display_markdown, IFrame

from pprint import pprint

def simulate_game():
    make_game_vis()

    time_limit_1 = 0.4
    time_limit_2 = 0.4

    board = game.ConnectFourBoard()
    player_1 = game.ComputerPlayer('alpha-beta', algo.alpha_beta_algo, time_limit_1)
    player_2 = game.ComputerPlayer('mcts', algo.mcts_algo, time_limit_2)
    sim = game.Simulation(board, player_1, player_2)
    sim.run(json_visualize=True)
    time.sleep(0.3)
    return sim.board.current_player_id()

def make_game_vis():
    frame = IFrame('vis/index.html', 490, 216)
    display(frame)

def run_final_test():
    losses = 0
    for i in xrange(1):
        winner = simulate_game()
        if winner != 0:
            losses += 1
            if losses > 1:
                lose()
                return
    win()

def win():
    display_markdown("""
Stonn sits back in shock, displaying far more emotion than any Vulcan should.

"Cadet, it looks like your thousands of years in the mud while we Vulcans
explored the cosmos were not in vain. Congratulations."

The class breaks into applause! Whoops and cheers ring through the air as
Captain James T. Kirk walks into the classroom to personally award you with
the Kobayashi Maru Award For Excellence In Tactics.

The unwelcome interruption of your blaring alarm clock brings you back to
reality, where in the year 2200 Earth's Daylight Savings Time was finally
abolished by the United Federation of Planets.""", raw=True)

def lose():
    display_html("""<div class="alert alert-failure">
    <strong>You can only lose once :(</strong>
    </div>""", raw=True)
