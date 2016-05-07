import game


class SnakeAction(game.Action):
    """
    This board represents an action in Snake.
    The actions specifies the color of the snake
    and its direction.
    Direction is defined as follow:
    1 - Left
    2 - Up
    3 - Right
    4 - Down
    """

    def __init__(self, color, direction):
        """
        params:
        color - a string from ['R', 'B'] that represents the color of the snake
        direction - an integer from [1,2,3,4] representing the direction to move the snake

        Functions needed:
        board.getSnakeCoords(color)
        board.setSnakeCoords(color, coordinates)
        board.hasFood(coordinate)
        """

        self.color = color
        self.direction = direction

    def apply(self, board):
        if not board.is_legal_action(self):
            raise Exception('This action is not allowed! => {}'.format(self))
          
        new_board = copy.copy(board)

        actionColor = board.BLACK
        if (self.color == "red"):
            actionColor = new_board.RED

        # Grab the coordinates of the snake segments
        oldSnakeCoords = new_board.getSnakeCoords(self.color) # NOTE: the 'head' of the snake is the first element in the array
        oldSnakeHead = snakeCoords[0]
        newSnakeHead = None

        # Calculate position of the snake head
        if (direction == 1): # move left
            newSnakeHead = (oldSnakeHead[0] - 1, oldSnakeHead[1])
        elif (direction == 2):# move up
            newSnakeHead = (oldSnakeHead[0], oldSnakeHead[1] + 1)
        elif (direction == 3): # move right
            newSnakeHead = (oldSnakeHead[0] + 1, oldSnakeHead[1])
        else: # move down
            newSnakeHead = (oldSnakeHead[0], oldSnakeHead[1] - 1)

        #If Snake is attempting to move to a non-empty square. Game Over.
        #This could be from running into itself, another snake, or off the map
        desiredLocationState = new_board.state[newSnakeHead[0]][newSnakeHead[1]]
        if (not(desiredLocationState == new_board.EMPTY)):
            #Here I determine the winning player, but I'm not sure if it should be done here!
            winner = "black"
            if (actionColor == new_board.BLACK):
                winner = "red"
            new_board._terminal_by_win() = True #Game should end before attempting to draw snake I think (or else it would glitch)


        # Create new snake
        newSnakeCoords = [newSnakeHead];
        for i in range(len(oldSnakeCoords)-1): #note, the final segment of the snake is dropped as it moves
            newSnakeCoords.append(oldSnakeCoords[i])
        # If the snake ate food, then we don't drop the final segment of the snake
        if (new_board.hasFood(newSnakeHead)):
            finalCoord = oldSnakeCoords[len(oldSnakeCoords)-1]
            newSnakeCoords.append(finalCoord)
            new_board.state[finalCoord[0]][finalCoord[1]] = actionColor
        else:
            new_board.state[finalCoord[0]][finalCoord[1]] = new_board.EMPTY
        #Color the location of the new snake head
        new_board.state[newSnakeHead[0]][newSnakeHead[1]] = actionColor

        new_board.last_move = (newSnakeHead) #not sure what to do for this yet?

        #update board with new snake coordinates
        new_board.setSnakeCoords(self.color, newSnakeCoords)

        return new_board

    def __hash__(self):
        return hash((self.color, self.direction))

    def __repr__(self):
        return 'SnakeAction(color={},direction={})'.format(self.color,self.direction)
