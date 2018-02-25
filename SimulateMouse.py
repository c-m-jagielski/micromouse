# simulate a mouse running through the maze
# this will be my main function

# imports
import argparse
from GenerateMaze import GenerateMaze

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
    generateMaze = GenerateMaze()
    generateMaze.createMaze(n)