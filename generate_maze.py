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
