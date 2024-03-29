# simulate a mouse running through the maze
# this will be my main function

# imports
import argparse, random
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
    REVERSE = 7
    F = FORWARD
    L = LEFT
    R = RIGHT
    V = REVERSE
    N = NORTH
    E = EAST
    S = SOUTH
    W = WEST

    def __init__(self, n=3):
        print("inside the simulation...")

        self.mazeSize = n  #can be 3x3 or 5x5

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
          print("Directional Error, bad input direction given:", currentDirection)
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

        d = "unk"
        if direction == self.N: d="North"
        elif direction == self.E: d="East"
        elif direction == self.S: d="South"
        elif direction == self.W: d="West"
        else: d="ERROR"
        print("***** oldSpot:", oldSpot, "direction:", d, "*****")

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
        print("ERROR in findNewSpot()")
        return 1

    def opposite(self, direction):
        """
        direction
          Input: L, R, F, or V
        """
        if direction == self.L: return self.R
        if direction == self.R: return self.L
        if direction == self.F: return self.V
        if direction == self.V: return self.F

    def optimizePath(self, inputMoves, deadends, spotList):
        """
        inputMoves
          Input: List of actions to take in each space; actions are integers (LEFT, RIGHT, FORWARD, REVERSE)

        deadends
          Input: List of dead-ends that were found

        spotList
          Input: List of spots we were at
        """

        optimizedPath = []

        print(" ")
        print("\t inputMoves", inputMoves)
        print("\t deadends  ", deadends)
        print("\t spotList  ", spotList)

        # we only need to optimize if we found a dead-end and had to reverse
        if len(deadends) == 0 and self.REVERSE not in inputMoves:
          print("Path optimization not necessary.\n")
          return inputMoves
        print("\nStarting path optimization...\n")
        print("inputMoves:    ", inputMoves)

        #for i in range(0,len(inputMoves)):
        #  print("  i:", i, "MOVE:", inputMoves[i], "   SPOT", spotList[i])
        #  #if inputMoves[i] is not 7 and spotList[i] not in deadends: continue

        # Find reversals, then remove that move and the previous move, and
        # Example:
        #     [4, 7, 5, 4, 5, 4, 5, 4, 7, 6]
        #     [      6, 4, 5, 4, 5,     , 5]
        optimizedPath = inputMoves
        while 1:
          # end the loop if all the reversals are gone
          if self.V not in optimizedPath: break

          i = optimizedPath.index(self.V)
          print("i: ", i)
          newMove = self.opposite(optimizedPath[i+1])
          print("newMove = ", newMove)
          optimizedPath[i+1] = newMove
          newOptPath = optimizedPath
          newOptPath.pop(i)
          newOptPath.pop(i-1)
          print("newOptPath:    ", newOptPath)

        return optimizedPath

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

        print("now discovering the best path...")
        bestPath = []  #initialize our return variable

        # iterate through the maze information and solve it!
        centerFound = 0  #stop when you find the center
        index = 0  #keep track of your index in the best path
        currentSpot = 6  #start at grid space #6 on our sample 3x3
        previousSpots = []  #track all spots in the maze we've been to
        myDirection = self.NORTH  #start by default facing North
        deadend = []  #track all dead-end spots

        # what is the center spot?
        center = -1
        if self.mazeSize == 3: center = 4
        elif self.mazeSize == 5: center = 99
        else:
          print("ERROR: maze size not supported")
          return

        while not centerFound:
          print("\n\nmaze step #", index, ":", mazeKnowledge[currentSpot])

          # store the spots to which we've been
          previousSpots.append(currentSpot)

          # get sensor data from the robot at the current spot
          wallsHere = mazeKnowledge[currentSpot]

          # walls are stored in global [N,E,S,W] frame of reference, not relative direction
          # which directions are available to move to?
          ahead, right, behind, left = self.availableMoves(myDirection, wallsHere)

          # are we in the center? Yes if behind us is the only open spot
          if behind and (not ahead and not right and not left):
            if currentSpot == center:
              print("Found the center!")
              centerFound = 1
              break
            else:
              print("Found a deadend at spot ", currentSpot)
              deadend.append(currentSpot)

          # what's possible? 15 total moves
          # F, R, V, L, FR, FL, FV, LR, RV, VL, FLR, FRV, FLV, LRV, FLRV
          #
          # what if you ignore what's open behind you (since you just came from there), unless reverse is the only option
          # F, R, L, V, FR, FL, LR, FLR

          # with randomness, go with whatever we find is open
          #TODO smartly choose one that we have not gone to before
          if ahead and right and left:
            # all options are available; do not go Reverse, that doesn't help
            r = random.randint(self.FORWARD, self.RIGHT)
            bestPath.append(r)
          elif ahead and left:
            r = random.randint(0, 1)
            if r==0: bestPath.append(self.FORWARD)
            else: bestPath.append(self.LEFT)
          elif ahead and right:
            r = random.randint(0, 1)
            if r==0: bestPath.append(self.FORWARD)
            else: bestPath.append(self.RIGHT)
          elif left and right:
            r = random.randint(0, 1)
            if r==0: bestPath.append(self.LEFT)
            else: bestPath.append(self.RIGHT)
          elif ahead: bestPath.append(self.FORWARD)
          elif right: bestPath.append(self.RIGHT)
          elif left: bestPath.append(self.LEFT)
          elif behind: bestPath.append(self.REVERSE)
          else: print("help me I'm trapped!")

          # turn based on the new movement to calculate new heading
          tmp = self.turn(myDirection, bestPath[index])
          myDirection = tmp
          #print("  new direction:", myDirection)

          # OK what is the next space going to be???
          tmp = self.findNewSpot(currentSpot, myDirection)
          #print("NEW current spot = ", currentSpot, "  ... guess = ", tmp)
          currentSpot = tmp

          index += 1

        #TODO now that I have _a_ path to the center, find the _best_ path to the center
        optimizedPath = self.optimizePath(bestPath, deadend, previousSpots)

        print("bestPath:      ", bestPath)
        print("optimizedPath: ", optimizedPath)
        return optimizedPath

if __name__ == "__main__":
    print("simulating the maze!")

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    parser.add_argument('-x', type=int, help='The example you want to run, e.g. 1 or 2.')
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

    example = 2
    if args.x:
        example = abs(args.x)

    # first generate the maze
    print("now generating the maze...")
    generateMaze = GenerateMaze()
    maze = generateMaze.createMaze(n, example)

    # now run the simulation
    sm = SimulateMouse(n)
    mazeKnowledge = sm.generateMazeMap(maze) #TODO this is the same as "generateMaze"
    #bestPath = sm.generateBestPath(mazeKnowledge) #TODO use if we get real robot information
    bestPath = sm.generateBestPath(maze)

    # for my first example 3x3, compare against the known solution:
    solutionExample = []
    if example==1:
      solutionExample = [sm.F,sm.F,sm.R,sm.F,sm.R,sm.F,sm.R,sm.R]
    elif example==2:
      solutionExample = [sm.R,sm.F,sm.L,sm.F,sm.L,sm.L]
    print("solution:      ", solutionExample)
    print("           F=4, L=5, R=6, V=7")

    # check for success
    success = 1
    for i in range(0, len(bestPath)):
      if bestPath[i] != solutionExample[i]:
        print("Error on step", i, "in the maze. Guessed", bestPath[i], "was", solutionExample[i])
        success = 0
        break
    if success: print("Success! We did it!")
