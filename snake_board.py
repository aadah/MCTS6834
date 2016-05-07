import game


class SnakeBoard(game.Board):
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

    def is_legal_action(self, action):
        """
        Returns True if the action is allowed
        to be performed on this board. False otherwise.

        params:
        action - the action to check
        """

        legal_actions = self.get_legal_actions()
        legal_actions = set([hash(act) for act in legal_actions])
        if hash(action) in legal_actions:
            return True
        return False

    def is_terminal(self):
        """
        Returns True if the state of the board
        is that of a finished game, False otherwise.
        """

        raise NotImplemented

    def reward_vector(self):
        """
        Returns the reward values for this state for each player
        as a tuple, with first player reward in 0th position,
        second player reward in 1st position, and so on.
        """

        raise NotImplemented

    def current_player_id(self):
        """
        Returns an integer id representing which player is to play next.
        """

        raise NotImplemented

    def visualize(self):
        """
        Visualize the board in some way or another.
        """

        raise NotImplemented

    def __copy__(self):
        raise NotImplemented
