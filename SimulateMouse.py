# simulate a mouse running through the maze
# this will be my main function

# imports
import argparse
from GenerateMaze import GenerateMaze

class SimulateMouse(object):
    """
    Simulate the mouse... go through the maze and map it out (discover walls) then solve the best path
    """

    # Define global variables
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    FORWARD = 4
    LEFT = 5
    RIGHT = 6
    REVERSE = 99
    F = FORWARD
    L = LEFT
    R = RIGHT
    V = REVERSE
    N = NORTH
    E = EAST
    S = SOUTH
    W = WEST

    def __init__(self):
        print("inside the simulation...")

    def generateMazeMap(self, maze):
        """
        Walk through the maze space-by-space to determine where the walls are.
        Output is a map describing the walls that have been discovered.

        maze
          Input: An array (n*n x 4 size) that tells the existence of walls for each position in the maze

        mazeKnowledge
          Output: Map describing the walls that have been discovered.
        """

        print("now the 'mouse' is mapping out the maze...")
        mazeKnowledge = []

        # mouse will iterate through the maze and map out every space we can
        centerFound = 0  #stop when you find the center
        index = 6  #keep track of your current spot, start at 6 for our sample 3x3 maze
        while not centerFound:
          #print "maze step:", maze[index]

          # TODO get sensor data from the robot

          index += 1
          # stop mapping out the maze walls after you find the center
          centerFound = 1

        return mazeKnowledge

    def turn(self, currentDirection, newMovement):
        """
        currentDirection
          Input: NORTH, EAST, SOUTH, WEST

        newMovement
          Input: FORWARD, LEFT, RIGHT, REVERSE

        Output: NORTH, EAST, SOUTH, WEST
        """

        if newMovement == self.FORWARD: return currentDirection

        if currentDirection == self.NORTH:
          if newMovement == self.LEFT: return self.WEST
          if newMovement == self.RIGHT: return self.EAST
          if newMovement == self.REVERSE: return self.SOUTH
        elif currentDirection == self.EAST:
          if newMovement == self.LEFT: return self.NORTH
          if newMovement == self.RIGHT: return self.SOUTH
          if newMovement == self.REVERSE: return self.WEST
        elif currentDirection == self.SOUTH:
          if newMovement == self.LEFT: return self.EAST
          if newMovement == self.RIGHT: return self.WEST
          if newMovement == self.REVERSE: return self.NORTH
        elif currentDirection == self.WEST:
          if newMovement == self.LEFT: return self.SOUTH
          if newMovement == self.RIGHT: return self.NORTH
          if newMovement == self.REVERSE: return self.EAST
        else:
          print "Directional Error, bad input direction given:", currentDirection
        return 0  # just default to North if something went wrong...

    def availableMoves(self, myDirection, wallsHere):
        """
          Walls are stored in global [N,E,S,W] frame of reference, not relative direction
          Which directions are available to move to?
        """

        ahead = right = behind = left = -99 #initialize vars
        if myDirection == self.NORTH:
          ahead = not wallsHere[0]
          right = not wallsHere[1]
          behind = not wallsHere[2]
          left = not wallsHere[3]
        if myDirection == self.EAST:
          left = not wallsHere[0]
          ahead = not wallsHere[1]
          right = not wallsHere[2]
          behind = not wallsHere[3]
        if myDirection == self.WEST:
          right = not wallsHere[0]
          behind = not wallsHere[1]
          left = not wallsHere[2]
          ahead = not wallsHere[3]
        if myDirection == self.SOUTH:
          behind = not wallsHere[0]
          left = not wallsHere[1]
          ahead = not wallsHere[2]
          right = not wallsHere[3]
        return [ahead, right, behind, left]

    def findNewSpot(self, oldSpot, direction):
        """
        Calcuate the new spot we're going to be in based on where we currently are and our movement will be

        oldSpot
          Input: current grid spot

          +--+--+--+
          | 0  1  2|
          +  +--+  +
          | 3| 4| 5|
          +  +  +  +
          | 6| 7  8|
          +--+--+--+

        direction
          Input: N, E, S, W

        Return: the new spot in the grid
        """

        #TODO set up for 5x5 grid, too

        if oldSpot == 0:
          if direction==self.E: return 1
          if direction==self.S: return 3
        elif oldSpot == 1:
          if direction==self.E: return 2
          if direction==self.S: return 4
          if direction==self.W: return 0
        elif oldSpot == 2:
          if direction==self.S: return 5
          if direction==self.W: return 1
        elif oldSpot == 3:
          if direction==self.N: return 0
          if direction==self.E: return 4
          if direction==self.S: return 6
        elif oldSpot == 4:
          if direction==self.N: return 1
          if direction==self.E: return 5
          if direction==self.S: return 7
          if direction==self.W: return 3
        elif oldSpot == 5:
          if direction==self.N: return 2
          if direction==self.S: return 8
          if direction==self.W: return 4
        elif oldSpot == 6:
          if direction==self.N: return 3
          if direction==self.E: return 7
        elif oldSpot == 7:
          if direction==self.N: return 4
          if direction==self.E: return 8
          if direction==self.W: return 6
        elif oldSpot == 8:
          if direction==self.N: return 5
          if direction==self.W: return 7
        else: pass
        print "ERROR in findNewSpot()"
        return 1

    def generateBestPath(self, mazeKnowledge):
        """
        Using the knowledge about the maze, solve for the optimum path through it.

        mazeKnowledge
          Input: Map describing the walls that have been discovered.
          Dictionary. Key is the space, value is a list of 0/1 for NEWS if a wall is present. Note -1 is used for unknown.
          Example: {0:[0,1,1,1], 1:[0,1,-1,1]} #this example is incomplete

        bestPath
          Output: List of actions to take in each space; actions are integers.
          Assume you start at the start/entry space in the maze.
          E.g. go forward 3 spaces, right 1 space, right 1 space, left, forward, left, forward, etc.
          'Forward' = 0
          'Left' = -1
          'Right = 1
        """

        print("now generating the best path...")

        #bestPath = [0,0,0,1,1,-1,0,-1,1]. #example
        bestPath = [7,7,7,7,7,7,7,7] # load with garbage

        # iterate through the maze information and solve it!
        centerFound = 0  #stop when you find the center
        index = 0  #keep track of your index in the best path
        currentSpot = 6  #start at grid space #6 on our sample 3x3
        previousSpots = []  #track all spots in the maze we've been to
        theAnswer = [6,3,0,1,2,5,8,7,4]
        myDirection = self.NORTH  #start by default facing North

        while not centerFound:
          print "maze step #", index, ":", mazeKnowledge[currentSpot]

          if index > 0:
            #TODO keep track of the new current spot...
            pass
          previousSpots.append(currentSpot)

          # get sensor data from the robot at the current spot
          wallsHere = mazeKnowledge[currentSpot]

          # walls are stored in global [N,E,S,W] frame of reference, not relative direction
          # which directions are available to move to?
          ahead, right, behind, left = self.availableMoves(myDirection, wallsHere)

          # are we in the center? Yes if behind us is the only open spot
          if behind and (not ahead and not right and not left):
            print "Found the center!"
            centerFound = 1
            break

          # what's possible? 15 total moves
          # N, E, S, W, NE, NW, NS, EW, ES, SW, NEW, NES, NWS, EWS, NEWS

          # dumb algorithm, just go with whatever we first find is open
          if ahead: bestPath[index] = self.FORWARD
          elif right: bestPath[index] = self.RIGHT
          elif left: bestPath[index] = self.LEFT
          elif behind: bestPath[index] = self.REVERSE
          else: print "help me!"

          # turn based on the new movement
          tmp = self.turn(myDirection, bestPath[index])
          myDirection = tmp
          print "  new direction:", myDirection

          index += 1

          # OK what is the next space going to be???
          currentSpot = theAnswer[index]
          tmp = self.findNewSpot(currentSpot, myDirection)
          print "NEW current spot = ", currentSpot, "  ... guess = ", tmp
          #currentSpot = tmp

        print "bestPath:", bestPath
        return bestPath

if __name__ == "__main__":
    print("simulating the maze!")

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    args = parser.parse_args()

    #print('args: %s'%(str(args)))

    # needs to be 3x3 or 5x5
    n = 3
    if args.n:
        n = args.n
    if n%2: pass
    else:
        n = n + 1
    if n > 5: n = 5
    if n < 3: n = 3

    # first generate the maze
    print("now generating the maze...")
    generateMaze = GenerateMaze()
    maze = generateMaze.createMaze(n)

    # now run the simulation
    sm = SimulateMouse()
    mazeKnowledge = sm.generateMazeMap(maze) #TODO this is the same as "generateMaze"
    #bestPath = sm.generateBestPath(mazeKnowledge) #TODO use if we get real robot information
    bestPath = sm.generateBestPath(maze)

    # for my first example 3x3, compare against the known solution:
    solutionExample1 = [sm.F,sm.F,sm.R,sm.F,sm.R,sm.F,sm.R,sm.R]
    print "solution:", solutionExample1

    # check for success
    success = 0
    for i in range(0, len(bestPath)):
      if bestPath[i] != solutionExample1[i]:
        print "Error on step", i, "in the maze. Guessed", bestPath[i], "was", solutionExample1[i]
        break
    if success: print("Success! We did it!")
