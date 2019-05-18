import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as pltcolours

#This is a python implementation of Langton's Ant

#There'll be a "Grid" object and an Ant object.
R = 1
L = -1
N = 128

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm

class Ant:
    def __init__(self, colours, position, orientation, rules):
        self.rules = rules
        self.position = position
        self.orientation = orientation
        self.colour = colours

#initialise once
class Colours:
    def __init__(self, numberOfColours):
        self.n = numberOfColours
        self.colours = [k for k in range(numberOfColours)]
    def getNext(self, current):
        return self.colours[(current + 1) % self.n]
    def __len__(self):
        return len(self.colours)

class Grid:
    def __init__(self, size = 64, orientation = 0, rules = 'LRRL'):
        # direction is a deque of fixed size which we rotate rotate to determine direction
        self.direction = deque([n for n in range(4)], 4)
        #rotate orientation to 0 -> we'll use position 0 to keep the current direction
        #and perform turning by rotating the deque in the appropriate direction
        while self.direction[0] != orientation: 
            self.direction.rotate(1)
        
        self.size = size
        #don't care about exact center
        self.rules = rules
        self.colours = Colours(len(rules))
        self.ant = Ant(len(rules), (int(size/2), int(size/2)), orientation, rules)
        self.state = np.zeros((size, size), dtype=np.uint8)
        self.setAntPosition((int(size/2), int(size/2)))

    def setAntPosition(self, position):
        #self.state.itemset(position, self.ant.colour)
        self.ant.position = position

    def getAntPosition(self):
        return self.ant.position

    def setPositionToColour(self, position, colour):
        self.state.itemset(position, colour)

    def getStates(self):
        return self.state

    def nextPosition(self, position, direction):
        if direction == 0:
            self.setAntPosition(((position[0] + 1) % self.size, position[1]))
        elif direction == 1:
            self.setAntPosition((position[0], (position[1] + 1) % self.size))
        elif direction == 2:
            self.setAntPosition(((position[0] - 1) % self.size, position[1]))
        elif direction == 3:
            self.setAntPosition((position[0], (position[1] - 1) % self.size))
    #this represents one turn in langton's ant
    def run(self):
        currentColour = self.state.item(self.getAntPosition())
        currentRule = self.rules[currentColour]
        if currentRule == 'R':
            self.direction.rotate(R)
        elif currentRule == 'L':
            self.direction.rotate(L)    
        
        newOrientation = self.direction[0]
        nextColour = self.colours.getNext(currentColour)
        ##set current
        self.setPositionToColour(self.getAntPosition(), nextColour)
        self.nextPosition(self.getAntPosition(), newOrientation)

def main():
    grid = Grid(N, 0, rules = 'RLR')
    fig = plt.figure()
    #normal = 
    img = plt.imshow(normalize(grid.getStates()), animated=True, vmin = 0, vmax = len(grid.colours) - 1, cmap='jet')

    def animate(i):
        grid.run() 
        cellsUpdated = grid.getStates().copy()
        #add ant position
        cellsUpdated.itemset(grid.getAntPosition(), grid.ant.colour)
        img.set_array(normalize(cellsUpdated))
        return img,

    interval = 20 #ms

    ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)

    plt.show()


if __name__ == '__main__':
    main()