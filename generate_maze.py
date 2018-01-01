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
    #print "maze:", maze

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
        maze[k][2] = 1 # South (bottom row)
        maze[k*n][3] = 1 #West (left side)
        maze[(k+1)*n-1][1] = 1 #East (right side)

if __name__ == "__main__":
    print "creating a maze"

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    args = parser.parse_args()

    #print 'args:', args

    n = 6
    if args.n:
        n = args.n

    createMaze(n)
