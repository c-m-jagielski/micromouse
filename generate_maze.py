# python code to create a maze

# imports
import argparse

def createMaze(n=6):
    print "Now creating a maze of size", n

    # Make the maze structure be a list of lists (nXn, where each "spot" has a 4x1 list of 0/1 for NESW if a wall is present)
    # First, initialize the maze.
    maze = []
    for k in range(0,n):
        for kk in range(0,n):
            maze.append([0,0,0,0])

    # The maze shall first start like this with the edges completed:
    #
    # +--+--+--+--+--+--+
    # |                 |
    # +  +  +  +  +  +  +
    # |                 |
    # +  +  +  +  +  +  +
    # |                 |
    # +  +  +  +  +  +  +
    # |                 |
    # +  +  +  +  +  +  +
    # |                 |
    # +  +  +  +  +  +  +
    # |                 |
    # +--+--+--+--+--+--+

    for k in range(0,n):
        maze[k][0] = 1 # North (top row)
        maze[n*n-1-k][2] = 1 # South (bottom row)
        maze[k*n][3] = 1 #West (left side)
        maze[(k+1)*n-1][1] = 1 #East (right side)

    # Fill in the center square walls with just 1 entrance
    maze[14] = [1,0,0,1]
    maze[15] = [1,1,0,0]
    maze[20] = [0,0,1,1]
    maze[21] = [0,1,0,0]

    #TODO: add in some algorithm to actually fill in the maze walls
    if n != 6:
        print "ERROR: only supports n=6 at this time."
        return

    #TODO: open one wall for the maze entrance
    #TODO: hard-code in other walls

    printMaze(maze, n)

def printMaze(maze, n):
    """
    A function to nicely print the maze out in a terminal
    """
    for k in range(0,n):
        tmp = ""
        for kk in range(0,n):
            tmp = tmp + str(maze[k*n+kk]) + " "
            #print "k", k, "kk", kk, "maze[k+kk] = ", maze[k+kk]
        print tmp
        print ""

if __name__ == "__main__":
    print "creating a maze"

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

    createMaze(n)
