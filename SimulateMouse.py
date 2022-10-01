# simulate a mouse running through the maze
# this will be my main function

# imports
import argparse
from GenerateMaze import GenerateMaze

class SimulateMouse(object):
    """
    Simulate the mouse... go through the maze and map it out (discover walls) then solve the best path
    """

    def __init__(self):
        print("inside simulation...")
        # TODO: do I need anything here?

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
          Input: North=0, East=1, South=2, West=3

        newMovement
          Input:
        """
        newDirection = -1

        if currentDirection == 0:
          if newMovement == 0: return 0
          if newMovement == 1: return 1
          if newMovement == 2: return 2
          if newMovement == 3: return 3
        elif currentDirection == 1:
          pass
        elif currentDirection == 2:
          pass
        elif currentDirection == 3:
          pass
        else:
          print "Directional Error, bad input direction given:", currentDirection

        return newDirection

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
        bestPath = [7,7,7,7,7,7,7,7,7] # load with garbage

        # iterate through the maze information and solve it!
        centerFound = 0  #stop when you find the center
        index = 0  #keep track of your index in the best path
        currentSpot = 6  #start at grid space #6 on our sample 3x3
        previousSpots = []  #track all spots in the maze we've been to
        theAnswer = [6,3,0,1,2,5,8,7,4]
        myDirection = 0  #North=0, East=1, South=2, West=3; start by default facing North

        while not centerFound:
          print "maze step #", index, ":", mazeKnowledge[currentSpot]

          if index > 0:
            #TODO keep track of the new current spot...
            pass
          previousSpots.append(currentSpot)

          # get sensor data from the robot at the current spot
          wallsHere = mazeKnowledge[currentSpot]

          next = -1 #start out we don't know what to do next

          # walls are [N,E,S,W]
          # which directions are available?
          ####Need to figure out what direction we're facing and then get this rotated

          north = not wallsHere[0]
          east = not wallsHere[1]
          south = not wallsHere[2]
          west = not wallsHere[3]

          # what's possible? 15 total moves
          # N, E, S, W, NE, NW, NS, EW, ES, SW, NEW, NES, NWS, EWS, NEWS

          # dumb algorithm, just go with whatever we first find is open
          # forward=0, right=1, left=1, backward=99
          if north: bestPath[index] = 0
          elif east: bestPath[index] = 1
          elif west: bestPath[index] = -1
          elif south: bestPath[index] = 99
          else: print "help me!"

          index += 1
          if index==9:
            centerFound = 1
            break

          # OK what is the next space going to be???
          # TODO figure this out another way? How should I get this feedback?
          currentSpot = theAnswer[index]

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
    simulateMouse = SimulateMouse()
    mazeKnowledge = simulateMouse.generateMazeMap(maze) #TODO this is the same as "generateMaze"
    #bestPath = simulateMouse.generateBestPath(mazeKnowledge) #TODO use if we get real robot information
    bestPath = simulateMouse.generateBestPath(maze)

    # for my first example 3x3, compare against the known solution:
    solutionExample1 = [0,0,1,0,1,0,1,1]
    print "solution:", solutionExample1

    # check for success
    success = 0
    for i in range(0, len(bestPath)):
      if bestPath[i] != solutionExample1[i]:
        print "Error on step", i, "in the maze. Guessed", bestPath[i], ", was", solutionExample1[i]
        break
    if success: print("Success! We did it!")
