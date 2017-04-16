from enum import Enum
import numpy as np


class InvalidMovement(Exception):
    pass


class SlidingMovement(Enum):
    """
    Performs a one-piece move from empty space
    """
    FROM_BOTTOM = 0
    FROM_TOP = 1
    FROM_LEFT = 2
    FROM_RIGHT = 3
    
    def __invert__(self):
        return {
            SlidingMovement.FROM_TOP: SlidingMovement.FROM_BOTTOM,
            SlidingMovement.FROM_BOTTOM: SlidingMovement.FROM_TOP,
            SlidingMovement.FROM_LEFT: SlidingMovement.FROM_RIGHT,
            SlidingMovement.FROM_RIGHT: SlidingMovement.FROM_LEFT
        }[self]


class SlidingPuzzle(object):
    
    def __init__(self, width=3, height=3, map=None):
        self.width = width
        self.height = height

        if map is None:
            self.map = np.asarray(range(height * width), dtype='uint8').reshape((height, width))
        else:
            self.map = map

        self.position = (0, 0)
    
    def move(self, movement):
        x0, y0 = self.position
        
        if movement == SlidingMovement.FROM_BOTTOM:
            if y0 == self.height - 1:
                raise InvalidMovement('Impossible slide FROM_BOTTOM')
            x1, y1 = x0, y0 + 1
        elif movement == SlidingMovement.FROM_TOP:
            if y0 == 0:
                raise InvalidMovement('Impossible slide FROM_TOP')
            x1, y1 = x0, y0 - 1
        elif movement == SlidingMovement.FROM_LEFT:
            if x0 == 0:
                raise InvalidMovement('Impossible slide FROM_LEFT')
            x1, y1 = x0 - 1, y0
        else:
            if x0 == self.width - 1:
                raise InvalidMovement('Impossible slide FROM_RIGHT')
            x1, y1 = x0 + 1, y0
        
        self.map[y0][x0], self.map[y1][x1] = self.map[y1][x1], self.map[y0][x0]
        
        self.position = (x1, y1)
    
    @property
    def possible_movements(self):
        x, y = self.position

        actions = []
        if y != 0:
            actions.append(SlidingMovement.FROM_TOP)
        if y != self.height - 1:
            actions.append(SlidingMovement.FROM_BOTTOM)
        if x != 0:
            actions.append(SlidingMovement.FROM_LEFT)
        if x != self.width - 1:
            actions.append(SlidingMovement.FROM_RIGHT)
        
        return actions

    def copy(self):
        puzzle_map = np.empty_like(self.map)
        np.copyto(puzzle_map, self.map)
        puzzle = SlidingPuzzle(self.width, self.height, map=puzzle_map)
        puzzle.position = (self.position[0], self.position[1])
        
        return puzzle
    
    def __repr__(self):
        return self.__str__
    
    def __str__(self):
        return str(self.map)

    @property
    def asarray(self):
        return self.map.flatten()

    def __eq__(self, other):
        return (self.asarray == other.asarray).all()

    def __hash__(self):
        return hash(str(self.asarray))
