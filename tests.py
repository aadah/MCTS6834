import IPython
from game import *
from nose.tools import assert_equal, ok_

def test_default_policy(default_policy):
    spy = Spy()
    board = SpyingConnectFourBoard(spy)
    # Set up a win in a column
    board.state = make_tied_state()
    board.state[4][2] = ConnectFourBoard.RED
    board.state[4][3] = ConnectFourBoard.RED
    board.state[4][4] = ConnectFourBoard.RED
    board.state[4][5] = ConnectFourBoard.EMPTY

    try:
        reward = default_policy(board)
        assert_equal(reward, (1, -1))

        application = spy.applications[-1]

        action = application[0]
        start_board = application[1]
        end_board = application[2]

        assert_equal(action.color, ConnectFourBoard.RED)
        assert_equal(action.col, 4)
        assert_equal(action.row, 5)

        assert_equal(start_board.state, board.state)

        board.state[4][5] = ConnectFourBoard.RED
        assert_equal(end_board.state, board.state)

        ok_(end_board.is_terminal())

        print_ok()
    except Exception as ex:
        print "Exception occured testing default_policy on board:"
        board.visualize()
        raise ex

def test_best_child(best_child):
    board = ConnectFourBoard()
    actions = list(board.get_legal_actions())

    parent = Node(board)
    children = [Node(action.apply(board), action, parent) for action in actions]
    parent.num_visits = len(children)

    for i in xrange(len(children)):
        child = children[i]
        child.q = (i+1)**2
        child.num_visits = i+1
        parent.add_child(child)

    # the last child will have the best value for c = 0
    best_correct_0 = parent.get_children()[-1]
    best_chosen_0 = best_child(parent, 0)

    # the last child will have the best value for c = 5
    best_correct_5 = parent.get_children()[0]
    best_chosen_5 = best_child(parent, 5)

    ok_(best_correct_0 is best_chosen_0)
    ok_(best_correct_5 is best_chosen_5)
    

def test_expand():
    pass

def test_tree_policy():
    pass

def test_backup():
    pass

def test_uct():
    pass

def print_ok():
    """ If execution gets to this point, print out a happy message """
    try:
        from IPython.display import display_html
        display_html("""<div class="alert alert-success">
        <strong>Tests passed!!</strong>
        </div>""", raw=True)
    except:
        print "Tests passed!!"

class Spy(object):

    def __init__(self):
        self.applications = []

def make_tied_state():
    state = make_empty_state()

    for col in xrange(ConnectFourBoard.NUM_COLS):
        for row in xrange(ConnectFourBoard.NUM_ROWS):
            piece = ConnectFourBoard.RED
            if (row / 2) % 2 == col % 2:
                piece = ConnectFourBoard.BLACK
            state[col][row] = piece
    return state

def make_empty_state():
    return [[ConnectFourBoard.EMPTY for j in xrange(ConnectFourBoard.NUM_ROWS)] for i in xrange(ConnectFourBoard.NUM_COLS)]

class SpyingConnectFourBoard(ConnectFourBoard):

    def __init__(self, spy, state=None, turn=None):
        self.spy = spy

        if state is None:
            self.state = [[ConnectFourBoard.EMPTY for j in xrange(ConnectFourBoard.NUM_ROWS)] for i in xrange(ConnectFourBoard.NUM_COLS)]
            self.turn = ConnectFourBoard.RED
        else:
            self.state = state
            self.turn = turn

        self.last_move = None

    def get_legal_actions(self):
        actions = set()

        for col in xrange(len(self.state)):
            column = self.state[col]
            for row in xrange(len(column)):
                if column[row] == ConnectFourBoard.EMPTY:
                    actions.add(SpyingConnectFourAction(self.spy, self.turn, col, row))
                    break

        return actions

    def __copy__(self):
        new_state = copy.deepcopy(self.state)
        return SpyingConnectFourBoard(self.spy, new_state, self.turn)

class SpyingConnectFourAction(ConnectFourAction):
    """
    This board represents an action in Connect Four.
    The actions specifies the color of the piece
    and the coordinate of where to place it.
    """

    def __init__(self, spy, color, col, row):
        """
        params:
        color - a string from ['R', 'B'] that represents the color of the piece
        col - integer for the column
        row - integer for the row
        """

        self.spy = spy
        self.color = color
        self.col = col
        self.row = row

    def apply(self, board):
        if not board.is_legal_action(self):
            raise Exception('This action is not allowed! => {}'.format(self))

        new_board = copy.copy(board)
        new_board.state[self.col][self.row] = self.color

        if self.color == ConnectFourBoard.RED:
            new_board.turn = ConnectFourBoard.BLACK
        else:
            new_board.turn = ConnectFourBoard.RED

        new_board.last_move = (self.col, self.row)

        self.spy.applications.append((self, board, new_board))

        return new_board

    def __hash__(self):
        return hash((self.color, self.col, self.row))
