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
        index = 0  #keep track of your current spot, start at 6 for our sample 3x3 maze
        while not centerFound:
          print "maze step:", maze[index]

          # TODO get sensor data from the robot

          index += 1
          centerFound = 1

        return mazeKnowledge

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
        bestPath = [0,0,0,0,0,0,0,0,0] # load with defaut

        # iterate through the maze information and solve it!
        #TODO

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

    # check for success
    success = 0
    for i in range(0, len(bestPath)):
      if bestPath[i] != solutionExample1[i]:
        print "Error on step", i, "in the maze. Guessed", bestPath[i], ", was", solutionExample1[i]
        break
    if success: print("Success! We did it!")
