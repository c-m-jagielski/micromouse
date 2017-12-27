# python code to create a maze

# imports
import argparse

def createMaze(n=6):
    print "Now creating a maze of size", n
    

if __name__ == "__main__":
    print "creating a maze"

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    args = parser.parse_args()

    print 'args:', args

    n = 6
    if args.n:
        n = args.n

    createMaze(n)