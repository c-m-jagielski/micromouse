"""
Micromouse Simulation System

This project creates a Python simulation environment for testing Micromouse C++ code.
It includes:
1. A maze simulation
2. C++ bindings using pybind11
3. Visualization tools

Project Structure:
- maze_simulator.py - Main simulation environment
- maze_generator.py - Class to build 4x4 and 16x16 maze layouts
- micromouse_wrapper.cpp - C++ wrapper with pybind11 bindings
- setup.py - Build script for C++ extensions
- #requirements.txt - Python dependencies
"""

# maze_simulator.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import animation
import time
import argparse
import os
import sys
from typing import List, Tuple, Dict, Optional

from maze_generator import MazeGenerator

# Import the C++ module (will be built using pybind11)
try:
    import micromouse_cpp
    print("c++ micromouse import successful")
except ImportError:
    print("C++ module not found. Please build it first with 'python setup.py build_ext --inplace'")
    print("Running in simulation-only mode")
    micromouse_cpp = None

class MazeSimulator:
    """A maze simulator for Micromouse testing."""

    def __init__(self, maze_layout=None):
        """Initialize the maze simulator.

        Args:
            maze_layout: Optional predefined maze layout. If None, a default maze is used.
        """
        self.size = 4  # 4x4 or 16x16
        self.cell_size = 100  # pixels

        # Initialize maze with all walls
        # walls[y][x] = [N, E, S, W] where 1 indicates a wall, 0 indicates no wall
        self.maze_generator = MazeGenerator()
        if maze_layout is None:
            # Default maze layout
            #    4: ["default", "simple", "complex"],
            #   16: ["classic", "random", "competition"]
            self.walls = self.maze_generator.generate_maze(self.size, "default")
        else:
            self.walls = maze_layout

        # Micromouse state
        self.mouse_position = (-1, 0)  # Start outside the maze, south of cell (0,0)
        self.mouse_heading = 0  # 0=North, 1=East, 2=South, 3=West

        # For visualization
        self.fig = None
        self.ax = None
        self.mouse_patch = None
        self.visited_cells = set()

        # Record of wall detections to pass to the C++ code
        self.detected_walls = {}
        numCells = self.size * self.size
        for i in range(numCells):
            self.detected_walls[i] = {}
            for ii in range(4):
                self.detected_walls[i][ii] = -1

        # Initialize outside walls
        self.detected_walls[0][2] = 1  # bottom-left corner
        self.detected_walls[0][3] = 1  # bottom-left corner
        self.detected_walls[self.size - 1][1] = 1  # bottom-right corner
        self.detected_walls[self.size - 1][2] = 1  # bottom-right corner
        self.detected_walls[numCells - self.size][0] = 1  # top-left corner
        self.detected_walls[numCells - self.size][3] = 1  # top-left corner
        self.detected_walls[numCells - 1][0] = 1  # top-right corner
        self.detected_walls[numCells - 1][1] = 1  # top-right corner
        for i in range(self.size - 2):
            # Bottom row, South walls
            self.detected_walls[i+1][2] = 1
            # Top row, North walls
            self.detected_walls[numCells - 1 - i][0] = 1
            # Left column, West walls
            self.detected_walls[self.size * (i+1)][3] = 1
            # Right column, East walls
            self.detected_walls[self.size * (i+2) - 1][1] = 1

        # Record of dead-end cells
        self.deadendCells = []

    def is_center(self, cell_idx: int) -> bool:
        """Check if a cell is in the center of the maze."""
        # Convert linear index to x,y coordinates
        x = cell_idx % self.size
        y = cell_idx // self.size

        # Center of a  4x4  maze is cells (1,1), (1,2), (2,1), (2,2)
        # Center of a 16x16 maze is cells (7,7), (7,8), (8,7), (8,8)
        if self.size == 4:
            return (x in [1, 2] and y in [1, 2])
        else:
            return (x in [7, 8] and y in [7, 8])

    def get_cell_linear_index(self, x: int, y: int) -> int:
        """Convert (x,y) coordinates to linear cell index."""
        return y * self.size + x

    def get_cell_coordinates(self, cell_idx: int) -> Tuple[int, int]:
        """Convert linear cell index to (x,y) coordinates."""
        x = cell_idx % self.size
        y = cell_idx // self.size
        return (x, y)

    def update_adjacent_wall(self, cell_x: int, cell_y: int, direction: int, wall_exists: bool):
        """Update the wall status for the adjacent cell in the opposite direction.

        Args:
            cell_x: X coordinate of the current cell
            cell_y: Y coordinate of the current cell
            direction: Direction of the wall from current cell (0=N, 1=E, 2=S, 3=W)
            wall_exists: Whether the wall exists
        """
        # Calculate coordinates of the adjacent cell
        adj_x, adj_y = cell_x, cell_y
        if direction == 0:  # North
            adj_y += 1
        elif direction == 1:  # East
            adj_x += 1
        elif direction == 2:  # South
            adj_y -= 1
        else:  # West
            adj_x -= 1

        # Ensure the adjacent cell is within the maze bounds
        if 0 <= adj_x < self.size and 0 <= adj_y < self.size:
            # Get the opposite direction
            opposite_direction = (direction + 2) % 4

            # Update the wall for the adjacent cell
            adj_cell_idx = self.get_cell_linear_index(adj_x, adj_y)
            if adj_cell_idx not in self.detected_walls:
                self.detected_walls[adj_cell_idx] = {}
            self.detected_walls[adj_cell_idx][opposite_direction] = wall_exists

    def detect_wall(self, cell_x: int, cell_y: int, direction: int) -> bool:
        """Check if there is a wall in the specified direction from the given cell."""
        # Make sure the cell is within bounds
        if not (0 <= cell_x < self.size and 0 <= cell_y < self.size):
            return True  # Treat out-of-bounds as walls

        # Get wall status
        wall_exists = self.walls[cell_y][cell_x][direction] == 1

        # Record the detection for the C++ code
        if 0 <= cell_x < self.size and 0 <= cell_y < self.size:
            cell_idx = self.get_cell_linear_index(cell_x, cell_y)
            if cell_idx not in self.detected_walls:
                self.detected_walls[cell_idx] = {}
            self.detected_walls[cell_idx][direction] = wall_exists
            self.update_adjacent_wall(cell_x, cell_y, direction, wall_exists)

        # Return wall status in the specified direction
        return wall_exists

    def move_mouse(self, direction: int) -> bool:
        """Move the micromouse in the specified direction if possible.

        Args:
            direction: 0=North, 1=East, 2=South, 3=West

        Returns:
            True if the move was successful, False if blocked by a wall
        """
        current_x, current_y = self.mouse_position

        # If starting outside the maze, special handling for entry
        if current_x == -1 and current_y == 0 and direction == 0:  # Entering from south
            self.mouse_position = (0, 0)
            self.mouse_heading = 0
            self.visited_cells.add((0, 0))
            return True

        # Check if there is a wall in the direction of movement
        if self.detect_wall(current_x, current_y, direction):
            return False

        # Calculate new position
        if direction == 0:  # North
            new_x, new_y = current_x, current_y + 1
        elif direction == 1:  # East
            new_x, new_y = current_x + 1, current_y
        elif direction == 2:  # South
            new_x, new_y = current_x, current_y - 1
        else:  # West
            new_x, new_y = current_x - 1, current_y

        # Check if new position is valid
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return False

        # Update position
        self.mouse_position = (new_x, new_y)
        self.visited_cells.add((new_x, new_y))
        return True

    def move_forward(self) -> bool:
        """Move the micromouse forward in the current heading direction."""
        result = self.move_mouse(self.mouse_heading)

        # Record the detection for the C++ code
        if self.mouse_position != (-1, 0):  # If not outside the maze
            x, y = self.mouse_position
            cell_idx = self.get_cell_linear_index(x, y)
            wall_detected = not result

            if cell_idx not in self.detected_walls:
                self.detected_walls[cell_idx] = {}

            self.detected_walls[cell_idx][self.mouse_heading] = wall_detected

        return result

    def turn_right(self):
        """Turn the micromouse 90° clockwise."""
        self.mouse_heading = (self.mouse_heading + 1) % 4

    def turn_left(self):
        """Turn the micromouse 90° counterclockwise."""
        self.mouse_heading = (self.mouse_heading + 3) % 4

    def turn_around(self):
        """Turn the micromouse 180°."""
        self.mouse_heading = (self.mouse_heading + 2) % 4

    def read_sensor(self) -> float:
        """Simulate reading from an ultrasonic sensor."""
        # Get current position and heading
        x, y = self.mouse_position

        # If outside the maze, return a large value (no wall)
        if x == -1 and y == 0:
            return 999.0 if self.mouse_heading == 0 else 10.0

        # Check if there's a wall in the current heading direction
        if self.detect_wall(x, y, self.mouse_heading):
            return 5.0  # Wall detected at 5cm distance
        else:
            return 30.0  # No wall within sensor range

    def initialize_visualization(self):
        """Set up the visualization of the maze and micromouse."""
        plt.ion()  # Enable interactive mode
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(-0.5, self.size - 0.5)
        self.ax.set_ylim(-0.5, self.size - 0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_title('Micromouse Simulation')
        self.ax.set_xticks(range(self.size))
        self.ax.set_yticks(range(self.size))

        # Draw the maze
        self._draw_maze()

        # Initialize mouse representation
        self.mouse_patch = Rectangle((-0.3, -0.3), 0.6, 0.6, color='red', alpha=0.7)
        self.ax.add_patch(self.mouse_patch)
        self._update_mouse_visualization()

        plt.tight_layout()
        plt.show()

    def _draw_maze(self):
        """Draw the maze walls."""
        for y in range(self.size):
            for x in range(self.size):
                # Check each wall direction
                if self.walls[y][x][0] == 1:  # North wall
                    self.ax.plot([x-0.5, x+0.5], [y+0.5, y+0.5], 'k-', linewidth=2)
                if self.walls[y][x][1] == 1:  # East wall
                    self.ax.plot([x+0.5, x+0.5], [y-0.5, y+0.5], 'k-', linewidth=2)
                if self.walls[y][x][2] == 1:  # South wall
                    self.ax.plot([x-0.5, x+0.5], [y-0.5, y-0.5], 'k-', linewidth=2)
                if self.walls[y][x][3] == 1:  # West wall
                    self.ax.plot([x-0.5, x-0.5], [y-0.5, y+0.5], 'k-', linewidth=2)

        # Mark the center of the maze
        center_x = (self.size - 1) / 2.0
        center_y = (self.size - 1) / 2.0
        self.ax.add_patch(plt.Rectangle((center_x-0.5, center_y-0.5), 1, 1, 
                                        color='green', alpha=0.2))

    def _update_mouse_visualization(self):
        """Update the micromouse's position and orientation in the visualization."""
        x, y = self.mouse_position

        # If outside the maze, position it below the starting position
        if x == -1 and y == 0:
            x, y = 0, -0.5

        # Update position
        self.mouse_patch.set_xy((x-0.3, y-0.3))

        # Update orientation (draw a line showing the heading)
        dx, dy = 0, 0
        if self.mouse_heading == 0:  # North
            dx, dy = 0, 0.2
        elif self.mouse_heading == 1:  # East
            dx, dy = 0.2, 0
        elif self.mouse_heading == 2:  # South
            dx, dy = 0, -0.2
        else:  # West
            dx, dy = -0.2, 0

        # Remove previous heading indicator
        for line in self.ax.lines:
            if hasattr(line, 'mouse_heading_indicator'):
                line.remove()

        # Draw new heading indicator
        line = self.ax.plot([x, x+dx], [y, y+dy], 'k-', linewidth=2)[0]
        line.mouse_heading_indicator = True

        # Color the visited cells
        for vx, vy in self.visited_cells:
            self.ax.add_patch(plt.Rectangle((vx-0.5, vy-0.5), 1, 1, 
                                           color='blue', alpha=0.1))

        # Update the display
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def run_simulation_step(self):
        """Run one step of the simulation."""
        # Get sensor reading
        distance = self.read_sensor()

        # Update visualization
        if self.fig is not None:
            self._update_mouse_visualization()
            plt.pause(0.1)

        # Return the distance reading
        return distance

    def run_simulation(self, steps=100, with_cpp=False):
        """Run the full simulation for a specified number of steps."""
        self.initialize_visualization()

        # Points for the center of the maze
        low = 1
        high = 2
        if self.size == 16:
            low = 7
            high = 8

        for step in range(steps):
            print(f"\nStep {step+1}/{steps}")
            print(f"Mouse position: {self.mouse_position}, heading: {self.mouse_heading}")

            # Run the C++ code if available
            if with_cpp and micromouse_cpp is not None:
                # Set up the state for the C++ code
                micromouse_cpp.set_position(self.get_cell_linear_index(*self.mouse_position))
                micromouse_cpp.set_heading(self.mouse_heading)

                # Run one step of the C++ algorithm
                micromouse_cpp.run_step(self.read_sensor())

                # Get the updated state from C++
                new_cell = micromouse_cpp.get_position()
                new_heading = micromouse_cpp.get_heading()

                # Convert linear index to coordinates
                new_x, new_y = self.get_cell_coordinates(new_cell)

                # Update mouse position and heading
                self.mouse_position = (new_x, new_y)
                self.mouse_heading = new_heading
            else:
                # Run built-in simulation logic
                self._run_builtin_algorithm()

            # Check if we've reached the center
            x, y = self.mouse_position
            if low <= x <= high and low <= y <= high:
                print("Reached the center of the maze!")
                plt.pause(2.0)
                print("\n\nHit CTRL+C to exit.\n")
                while 1: plt.pause(5.0)

            # Update visualization
            self._update_mouse_visualization()
            plt.pause(0.4)  # Slow down the simulation for visibility

        plt.ioff()
        plt.show()

    def _run_builtin_algorithm(self):
        """A simple wall-following algorithm that prioritizes unexplored spaces."""
        x, y = self.mouse_position
        cell_idx = self.get_cell_linear_index(x, y)
        maxCell = self.size * self.size - 1

        # Starting out, we must go forward to enter the maze
        if cell_idx == -1:
            self.move_forward()
            return

        # Get the current state of walls around the cell
        wallInFront = 1 if self.read_sensor() < 10 else 0

        wallToTheLeft = -1
        wallToTheRight = -1
        wallBehindMe = -1

        if cell_idx in self.detected_walls:
            leftHeading = (self.mouse_heading + 3) % 4
            rightHeading = (self.mouse_heading + 1) % 4
            behindMeHeading = (self.mouse_heading + 2) % 4

            # Get wall status in each direction if known
            if leftHeading in self.detected_walls[cell_idx]:
                wallToTheLeft = self.detected_walls[cell_idx][leftHeading]
            if rightHeading in self.detected_walls[cell_idx]:
                wallToTheRight = self.detected_walls[cell_idx][rightHeading]
            if behindMeHeading in self.detected_walls[cell_idx]:
                wallBehindMe = self.detected_walls[cell_idx][behindMeHeading]

        # Calculate adjacent cell indices
        frontCellIdx = -1
        leftCellIdx = -1
        rightCellIdx = -1
        backCellIdx = -1

        # Calculate front cell
        if self.mouse_heading == 0:  # North
            frontCellIdx = cell_idx + self.size if cell_idx + self.size <= maxCell else -1
            leftCellIdx = cell_idx - 1 if cell_idx % self.size > 0 else -1
            rightCellIdx = cell_idx + 1 if (cell_idx + 1) % self.size > 0 else -1
            backCellIdx = cell_idx - self.size if cell_idx - self.size >= 0 else -1
        elif self.mouse_heading == 1:  # East
            frontCellIdx = cell_idx + 1 if (cell_idx + 1) % self.size > 0 else -1
            leftCellIdx = cell_idx + self.size if cell_idx + self.size <= maxCell else -1
            rightCellIdx = cell_idx - self.size if cell_idx - self.size >= 0 else -1
            backCellIdx = cell_idx - 1 if cell_idx % self.size > 0 else -1
        elif self.mouse_heading == 2:  # South
            frontCellIdx = cell_idx - self.size if cell_idx - self.size >= 0 else -1
            leftCellIdx = cell_idx + 1 if (cell_idx + 1) % self.size > 0 else -1
            rightCellIdx = cell_idx - 1 if cell_idx % self.size > 0 else -1
            backCellIdx = cell_idx + self.size if cell_idx + self.size <= maxCell else -1
        else:  # West
            frontCellIdx = cell_idx - 1 if cell_idx % self.size > 0 else -1
            leftCellIdx = cell_idx - self.size if cell_idx - self.size >= 0 else -1
            rightCellIdx = cell_idx + self.size if cell_idx + self.size <= maxCell else -1
            backCellIdx = cell_idx + 1 if (cell_idx + 1) % self.size > 0 else -1

        # Check which adjacent cells have been visited
        frontVisited = False
        leftVisited = False
        rightVisited = False
        backVisited = False

        if frontCellIdx != -1:
            frontCoords = self.get_cell_coordinates(frontCellIdx)
            if frontCoords in self.visited_cells:
                frontVisited = True

        if leftCellIdx != -1:
            leftCoords = self.get_cell_coordinates(leftCellIdx)
            if leftCoords in self.visited_cells:
                leftVisited = True

        if rightCellIdx != -1:
            rightCoords = self.get_cell_coordinates(rightCellIdx)
            if rightCoords in self.visited_cells:
                rightVisited = True

        if backCellIdx != -1:
            backCoords = self.get_cell_coordinates(backCellIdx)
            if backCoords in self.visited_cells:
                backVisited = True

        # Determine possible moves based on walls
        possibleMoves = []
        if wallInFront in [0, -1] and frontCellIdx != -1:
            possibleMoves.append(('forward', frontVisited))
        if wallToTheRight in [0, -1] and rightCellIdx != -1:
            possibleMoves.append(('right', rightVisited))
        if wallBehindMe in [0, -1] and backCellIdx != -1:
            possibleMoves.append(('back', backVisited))
        if wallToTheLeft in [0, -1] and leftCellIdx != -1:
            possibleMoves.append(('left', leftVisited))

        # Check if we're currently in a dead end
        if len(possibleMoves) == 1:
            if cell_idx not in self.deadendCells:
                self.deadendCells.append(cell_idx)

        # No possible moves (this shouldn't happen in a valid maze)
        if not possibleMoves:
            print("No possible moves! Turning around.")
            self.turn_around()
            return

        # Prioritize unexplored cells
        unvisitedMoves = [move for move, visited in possibleMoves if not visited]

        if unvisitedMoves:
            # We have unexplored options - choose the first one
            move = unvisitedMoves[0]
        else:
            # All options lead to visited cells - just pick the first one
            move = possibleMoves[0][0]

        # Execute the chosen move
        print(f"Choosing move: {move}")
        if move == 'forward':
            self.move_forward()
        elif move == 'right':
            self.turn_right()
            self.move_forward()
        elif move == 'left':
            self.turn_left()
            self.move_forward()
        elif move == 'back':
            self.turn_around()
            self.move_forward()

    def export_to_cpp(self) -> Dict:
        """Export the current maze state to a format usable by the C++ code."""
        result = {
            'size': self.size,
            'walls': self.walls,
            'detected_walls': self.detected_walls
        }
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Micromouse Maze Simulator')
    parser.add_argument('--steps', type=int, default=250, help='Number of simulation steps')
    parser.add_argument('--cpp', action='store_true', help='Use C++ algorithm')
    args = parser.parse_args()

    # Create and run the simulation
    simulator = MazeSimulator()
    simulator.run_simulation(steps=args.steps, with_cpp=args.cpp)