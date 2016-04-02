import math
import copy


class Board(object):
    """
    This class represents an instantaneous board
    state of a game in progress. Should be able
    to be copied to keep track of board histories.
    """

    def __init__(self):
        raise NotImplemented

    def get_legal_actions(self):
        """
        Return a set of legal actions that can be
        on this current board.
        """

        raise NotImplemented

    def is_terminal(self):
        """
        Returns True if the state of the board
        is that of a finished game, False otherwise.
        """

        raise NotImplemented

    def __copy__(self):
        raise NotImplemented


class ConnectFourBoard(Board):
    """
    This class represents a Connect Four board.
    Locations are accessed via a 0-indexed coordinate system.
    Coordinate (x,y) means row y of column x.
    Bottom row is row 0.
    Being a two-player game, we have Red and Black
    moves, represented as R and B respectively.
    The symbol '-' means no piece is at that coordinate.
    """
    RED = 'R'
    BLACK = 'B'
    EMPTY = '-'
    NUM_COLS = 6
    NUM_ROWS = 7

    def __init__(self, state=None, turn=None):
        """
        params:
        state - the board state represented as nested lists
        turn - which color is to play next. either RED or BLACK
        """

        if state is None:
            self.state = [[EMPTY for j in xrange(NUM_COLS)] for i in xrange(NUM_ROWS)]
            self.turn = RED
        else:
            self.state = state
            self.turn = turn
        
    def get_legal_actions(self):
        actions = set()
        
        for col in xrange(len(self.state)):
            column = self.state[col]
            for row in xrange(len(column)):
                if column[row] == EMPTY:
                    action.add(ConnectFourAction(self.turn, col, row))
                    break

        return actions

    def is_terminal(self):
        pass

    def __copy__(self):
        new_state = copy.deepcopy(self.state)
        
        return ConnectFourBoard(new_state, self.turn)


class Action(object):
    """
    This class represents a generic action that
    can be performed on a certain board.
    Needs to be hashable in order
    to distinguish from other possible
    actions for the same board.
    """

    def __init__(self):
        raise NotImplemented

    def apply(board):
        """
        Applies the action to the board and returns a new board
        that results from it.
        Throws an error if action cannot be applied.
        """

        raise NotImplemented
        
    def __hash__(self):
        raise NotImplemented


class ConnectFourAction(Action):
    """
    This board represents an action in Connect Four.
    The actions specifies the color of the piece
    and the coordinate of where to place it.
    """

    def __init__(self, color, col, row):
        """
        params:
        color - a string from ['R', 'B'] that represents the color of the piece
        col - integer for the column
        row - integer for the row
        """

        self.color = color
        self.col = col
        self.row = row

    def apply(board):
        legal_actions = board.get_legal_actions()
        if self not in legal_actions:
            raise Exception("This action is not allowed!")
            
        new_board = copy.copy(board)
        new_board.state[self.col][self.row] = self.color

        if self.color == ConnectFourBoard.RED:
            new_board.turn = ConnectFourBoard.BLACK
        else:
            new_board.turn = ConnectFourBoard.RED

        return board

    def __hash__(self):
        return hash((self.color, self.col, self.row))


class Player(object):
    """
    This class represents a player.
    Subclasses can be human agents
    that takes input, or programs
    that run an algorithm.
    """

    def __init__(self):
        raise NotImplemented

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


class Game(object):
    """
    This classes represents and simulates a game
    between two players.
    """

    def __init__(self, init_board, player_1, player_2):
        self.board = init_board
        self.player_1 = player_1
        self.player_2 = player_2

    def run(self):
        pass
        #while not board


class Node(object):
    def __init__(self, action, board, parent=None):
        """
        Create new node in MCTS tree.

        params:
        action - Incoming action that created this node.
        board - Board state that this node represents.
        parent - Parent node. Is None for root.
        """

        self.action = action
        self.board = board
        self.parent = parent
        self.children = [] # children nodes
        self.num_visits = 0 # number of times node has been visited
        self.q = 0.0 # simulation reward
        
    def get_action(self):
        """
        Return associated incoming action.
        """
        
        return self.action

    def get_board(self):
        """
        Returns associated board state.
        """

        return self.board
        
    def get_parent(self):
        """
        Return parent node.
        """

        return self.parent

    def get_children(self):
        """
        Return children nodes.
        """
        
        return self.children

    def add_child(self, child):
        """
        Adds a new child node to the nodes visited children.
        """

        self.children.append(child)

    def get_num_visits(self):
        """
        Return number of time this node has been visited.
        """

        return self.num_visits

    def q_value(self):
        """
        Return the simulation Q value reward.
        """

        return self.q

    def visit(self):
        """
        Increment visit counter.
        """

        self.num_visits += 1

    def is_fully_expanded(self):
        """
        Returns True if the node has
        all possible children in self.children,
        False otherwise.
        """
        
        possible_actions = self.board.get_legal_actions()
        taken_actions = set([child.action for child in self.children])
        untaken_actions = possible_actions ^ taken_actions
        
        return len(untaken_actions) == 0

    def value(self, c):
        """
        Return the UCT heuristic value of the node.

        params:
        c - exploration value. Larger values encourage exploration of tree.
        """

        exploitation_value = self.q / self.num_visits
        exploration_value = c * math.sqrt(2 * math.log(self.parent.num_visits) / self.num_visits)
        
        return exploitation_value + exploration_value
