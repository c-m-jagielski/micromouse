# python code to create a maze

# imports
import argparse

class GenerateMaze(object):

    def createMaze(self, n=6):
        print("Now creating a maze of size %i"%(n))

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
            print("ERROR: only supports n=6 at this time.")
            return

        # Open one wall for the maze entrance (choose South wall on bottom row)
        maze[(n*n-1)-1][2] = 0

        # Hard-code in other walls
        maze[0][2] = 1
        maze[2][2] = 1
        maze[4][1] = 1
        maze[5][3] = 1

        maze[6][0] = 1
        maze[6][2] = 1
        maze[7][1] = 1
        maze[8][0] = 1
        maze[8][2] = 1
        maze[8][3] = 1
        maze[9][1] = 1
        maze[9][2] = 1
        maze[10][2] = 1
        maze[10][3] = 1

        maze[12][0] = 1
        maze[12][2] = 1
        maze[13][1] = 1
        maze[16][0] = 1
        maze[16][2] = 1
        maze[16][3] = 1

        maze[18][0] = 1
        maze[18][2] = 1
        maze[19][1] = 1
        maze[22][0] = 1
        maze[22][2] = 1
        maze[22][3] = 1

        maze[24][0] = 1
        maze[26][0] = 1
        maze[26][2] = 1
        maze[27][1] = 1
        maze[27][2] = 1
        maze[28][0] = 1
        maze[28][3] = 1

        maze[30][1] = 1
        maze[31][1] = 1
        maze[31][3] = 1
        maze[32][0] = 1
        maze[32][3] = 1
        maze[33][0] = 1
        maze[34][1] = 1
        maze[35][3] = 1

        self.printMaze(maze, n)

    def printMaze(self, maze, n):
        """
        A function to nicely print the maze out in a terminal
        """
        for k in range(0,n):
            tmp = ""
            for kk in range(0,n):
                tmp = tmp + str(maze[k*n+kk]) + " "
                #print "k", k, "kk", kk, "maze[k+kk] = ", maze[k+kk]. #TODO update print statement
            print(tmp)
            print("")

if __name__ == "__main__":
    print("creating a maze")

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-n', type=int, help='The size of the maze, should be an even number.')
    args = parser.parse_args()

    #print('args: %s'%(str(args)))

    n = 6
    if args.n:
        n = args.n
    if n%2:
        n = n + 1
    if n < 6:
        n = 6

    generateMaze = GenerateMaze()
    generateMaze.createMaze(n)
