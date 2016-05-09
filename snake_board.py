import copy
import random

import game
from snake_action import *


class SnakeBoard(game.Board):
    RED = 'R'
    BLACK = 'B'
    WIDTH = 40#80
    HEIGHT = 25#50
    NUM_FOOD_ITEMS = 10

    def __init__(self, state=None, turn=None):
        if state == None:
            state = {}
            red_snake = (3, [(3,1),
                             (2,1),
                             (1,1)])
            black_snake = (1, [(SnakeBoard.WIDTH-4,SnakeBoard.HEIGHT-2),
                               (SnakeBoard.WIDTH-3,SnakeBoard.HEIGHT-2),
                               (SnakeBoard.WIDTH-2,SnakeBoard.HEIGHT-2)])
            food = set([(random.randint(0, SnakeBoard.WIDTH-1),
                         random.randint(0, SnakeBoard.HEIGHT-1)) for i in xrange(SnakeBoard.NUM_FOOD_ITEMS)])
            state['width'] = SnakeBoard.WIDTH
            state['height'] = SnakeBoard.HEIGHT
            state[SnakeBoard.RED] = red_snake
            state[SnakeBoard.BLACK] = black_snake
            state['food'] = food
            self.state = state
            self.turn = SnakeBoard.RED
        else:
            self.state = state
            self.turn = turn

    def get_legal_actions(self):
        actions = set()
        direction, _ = self.state[self.turn]
        
        for next_direction in [1,2,3,4]:
            if next_direction != direction and next_direction % 2 == direction % 2:
                continue # going backwards is not allowed
            action = SnakeAction(self.turn, next_direction)
            actions.add(action)

        return actions

    def _is_border_collision(self, coor):
        x, y = coor
        x_out = x < 0 or x >= SnakeBoard.WIDTH
        y_out = y < 0 or y >= SnakeBoard.HEIGHT

        return x_out or y_out

    def is_terminal(self):
        illegal_positions = set()
        _, red_snake = self.state[SnakeBoard.RED]
        _, black_snake = self.state[SnakeBoard.BLACK]

        if self.turn == SnakeBoard.RED:
            illegal_positions.update(red_snake)
            illegal_positions.update(black_snake[1:])
            coor = black_snake[0]
        else:
            illegal_positions.update(red_snake[1:])
            illegal_positions.update(black_snake)
            coor = red_snake[0]
        
        return coor in illegal_positions or self._is_border_collision(coor)

    def reward_vector(self):
        if self.is_terminal():
            end_game_val = 1000000.0

            if self.turn == SnakeBoard.RED:
                return (end_game_val,-end_game_val)
            else:
                return (-end_game_val,end_game_val)

        length_scale_factor = 10.0
        red_length = len(self.state[SnakeBoard.RED][1])
        black_length = len(self.state[SnakeBoard.BLACK][1])
        diff = (red_length - black_length) * length_scale_factor

        return (diff, -diff)

    def current_player_id(self):
        if self.turn == SnakeBoard.RED:
            return 0
        else:
            return 1

    def visualize(self):
        grid = [[" " for j in xrange(self.state['width'])] for i in xrange(self.state['height'])]
        for item in self.state['food']:
            grid[item[1]][item[0]] = '@'
        
        _, red_snake = self.state[SnakeBoard.RED]
        _, black_snake = self.state[SnakeBoard.BLACK]
        
        for coor in red_snake:
            x, y = coor
            grid[y][x] = SnakeBoard.RED
        
        for coor in black_snake:
            x, y = coor
            grid[y][x] = SnakeBoard.BLACK

        grid[red_snake[0][1]][red_snake[0][0]] = '+'
        grid[black_snake[0][1]][black_snake[0][0]] = 'x'

        print ''.join(['_' for i in xrange(self.state['width'] + 2)])

        for i in xrange(self.state['height']):
            print '|' + ''.join(grid[self.state['height'] - i -1]) + '|'

        print ''.join(['-' for i in xrange(self.state['width'] + 2)])

        print
        

    def __copy__(self):
        new_state = copy.deepcopy(self.state)
        
        return SnakeBoard(new_state, self.turn)

    def get_snake(self, color):
        return self.state[color]

    def set_snake(self, color, direction, coors):
        self.state[color] = (direction, coors)

    def has_food(self, coor):
        return coor in self.state['food']

    def get_food(self):
        return self.state['food']

    def switch_turn(self, color):
        if color == SnakeBoard.RED:
            self.turn = SnakeBoard.BLACK
        else:
            self.turn = SnakeBoard.RED
