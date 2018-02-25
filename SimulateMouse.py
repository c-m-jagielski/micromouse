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
        print "inside simulation..."
        # TODO: do I need anything here?

    def generateMazeMap(self, maze):
        """
        maze
          An array (n*n x 4 size) that tells the existence of walls for each position in the maze
        """
        print "now the 'mouse' is mapping out the maze..."
        mazeKnowledge = []
        return mazeKnowledge

    def generateBestPath(self, mazeKnowledge):
        print "now generating the best path..."
        bestPath = []
        return bestPath

if __name__ == "__main__":
    print "simulating the maze!"

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    args = parser.parse_args()

    #print 'args:', args

    n = 6
    if args.n:
        n = args.n
    if n%2:
        n = n + 1
    if n < 6:
        n = 6

    # first generate the maze
    print "now generating the maze..."
    generateMaze = GenerateMaze()
    maze = generateMaze.createMaze(n)

    # now run the simulation
    simulateMouse = SimulateMouse()
    mazeKnowledge = simulateMouse.generateMazeMap(maze)
    bestPath = simulateMouse.generateBestPath(mazeKnowledge)