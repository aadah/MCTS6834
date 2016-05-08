import game
from snake_action import *


class SnakePlayer(game.HumanPlayer):
    """
    Human player that plays Snake.
    """

    def choose_action(self, board):
        action = None
        
        #if no move from joystick: go into Board class and get last move 
        while action is None:
            next_dir = self.source() # returns 0,1,2,3,4, representing the direction the person wants to go

            curr_dir = board.get_snake(color)[0] #current direction the snake is going
            
            #if human isn't holidng the joystick in any direction
            if (next_dir == 0):
                action = SnakeAction(board.turn, curr_dir)

            #if the next direction is oppositive from curr_dir,
            #new direction is the direction the snake is already going
            if ((next_dir == 1) && (curr_dir == 3)) or ((next_dir == 3) && (curr_dir == 1)):
                action = SnakeAction(board.turn, curr_dir)
            if ((next_dir == 2) && (curr_dir == 4)) or ((next_dir == 4) && (curr_dir == 2)):
                action = SnakeAction(board.turn, curr_dir)
            else:
                action = SnakeAction(board.turn, next_dir)
          
            if not board.is_legal_action(action):
                #print '{} is not a legal action on this board.'.format(action)
                action = None

        return action
