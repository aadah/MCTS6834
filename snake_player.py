import game

class Player(object):
    """
    This class represents a player.
    Subclasses can be human agents
    that takes input, or programs
    that run an algorithm.
    """

    def __init__(self, name):
        self.name = name

    def choose_action(self, board):
        """
        Returns an action that the player
        wishes to perform on the board.

        params:
        board -  the current board
        """

        raise NotImplemented

    def play_action(self, action, board):
        """
        Player performs an action
        on a given board.
        Returns the new board that results from it.

        params:
        action - the action that the player wishes to perform
        board - the current board
        """

        new_board = action.apply(board)

        return new_board

class HumanPlayer(Player):
    """
    A generic human player that takes
    a source function that returns some
    representation of the human's
    action.
    """

    def __init__(self, name, source):
        Player.__init__(self, name)
        self.source = source

class SnakePlayer(game.Player):
    """
    Human player that plays Snake.
    """

    def choose_action(self, board):
        action = None
        
        #if no move from joystick: go into Board class and get last move 
        while action is None:
            width, height = self.source() # example of how input comes from the source

            if width >= 0 and width < SnakeBoard.WIDTH and height >= 0 and height < SnakeBoard.HEIGHT:
                action = SnakeAction(color, direction)
            else:
                print 'Coordinate out of range: 0 <= WIDTH <= {}, 0 <= HEIGHT <= {}'.format(ConnectFourBoard.NUM_COLS-1, ConnectFourBoard.NUM_ROWS-1)

            if not board.is_legal_action(action):
                print '{} is not a legal action on this board.'.format(action)
                action = None

        return action
