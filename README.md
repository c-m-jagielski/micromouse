# micromouse
Various code for micromouse

Micromouse is an international competition where robot "mice" compete to quickly find their way through a center of a maze. First the mouse has to investigate the maze and identify the location of its center, and then on the next run it has to take the optimum path from the maze start to the maze center as quickly as possible.

Code components:
 * generate a maze
 * search/map maze
 * find maze center
 * solve for best path to center (Flood fill?)

# TODO list
What's on the docket?
 * add real unit tests into test_class for pytest to use
 * add pre-built mazes of multiple sizes (to enable repeatable testing)
 * make a mechanism to generate a random maze (must follow maze rules)
 * add an actual UI to display the maze
 * incorporate an algorithm to find the maze center
 * incorporate an algorithm to solve for the best path (shortest distance) to the center
 * include hooks for hardware (c2 for the robotic 'mouse')
