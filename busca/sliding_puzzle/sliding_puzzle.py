from enum import Enum

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
    
    def __init__(self, width=3, height=3):
        self.width = width
        self.height = height
        
        self.map = [[i*width + j for j in range(width)] for i in range(height)]
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
        puzzle = SlidingPuzzle(self.width, self.height)
        puzzle.position = (self.position[0], self.position[1])
        puzzle.map = [row[:] for row in self.map]
        
        return puzzle
    
    def __repr__(self):
        return self.__str__
    
    def __str__(self):
        digit_size = str(len(str(self.width * self.height)))
        
        text = '\n'
        for line in self.map:
            for element in line:
                if element == 0:
                    element = ' '
                
                text += ('{:>'+digit_size+'} ').format(element)
            text += '\n'

        return text

    @property
    def asarray(self):
        return [element for line in self.map for element in line]

    def __eq__(self, other):
        return self.asarray == other.asarray

    def __hash__(self):
        return hash(tuple(self.asarray))