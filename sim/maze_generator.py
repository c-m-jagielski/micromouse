import numpy as np
from typing import List, Dict, Tuple, Optional
import random


class MazeGenerator:
    """
    A flexible maze generator for Micromouse simulations that supports
    multiple maze sizes (4x4 and 16x16) and different layout options.
    """

    def __init__(self):
        """Initialize the maze generator with available layouts."""
        # Register available maze layouts by size
        self.available_layouts = {
            4: ["default", "simple", "complex"],
            16: ["classic", "random", "competition"]
        }

    def generate_maze(self, size: int, layout_type: str = None) -> List[List[List[int]]]:
        """
        Generate a maze of specified size and layout type.

        Args:
            size: Size of the maze (4 or 16)
            layout_type: Type of layout to generate. If None, a random layout is chosen.

        Returns:
            3D list representing the maze walls where walls[y][x] = [N, E, S, W]
            with 1 indicating a wall and 0 indicating no wall
        """
        if size not in self.available_layouts:
            raise ValueError(f"Unsupported maze size: {size}. Supported sizes: {list(self.available_layouts.keys())}")

        # If no layout specified, choose a random one
        if layout_type is None:
            layout_type = random.choice(self.available_layouts[size])
        elif layout_type not in self.available_layouts[size]:
            raise ValueError(f"Unsupported layout type '{layout_type}' for size {size}. "
                           f"Available layouts: {self.available_layouts[size]}")

        # Generate the requested maze
        if size == 4:
            return self._generate_4x4_maze(layout_type)
        else:  # size == 16
            return self._generate_16x16_maze(layout_type)

    def _generate_4x4_maze(self, layout_type: str) -> List[List[List[int]]]:
        """Generate a 4x4 maze with the specified layout type."""
        if layout_type == "default":
            return self._create_4x4_default_maze()
        elif layout_type == "simple":
            return self._create_4x4_simple_maze()
        elif layout_type == "complex":
            return self._create_4x4_complex_maze()
        else:
            raise ValueError(f"Unknown 4x4 layout type: {layout_type}")

    def _generate_16x16_maze(self, layout_type: str) -> List[List[List[int]]]:
        """Generate a 16x16 maze with the specified layout type."""
        if layout_type == "classic":
            return self._create_16x16_classic_maze()
        elif layout_type == "random":
            return self._create_16x16_random_maze()
        elif layout_type == "competition":
            return self._create_16x16_competition_maze()
        else:
            raise ValueError(f"Unknown 16x16 layout type: {layout_type}")

    def _create_4x4_default_maze(self) -> List[List[List[int]]]:
        """Create the default 4x4 maze layout."""
        size = 4
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Remove some walls to create a solvable maze
        # Format: walls[y][x] = [N, E, S, W]

        # Opening at the start (south of bottom-left cell)
        walls[0][0][2] = 0  # Remove south wall of (0,0)

        # Create a path to the center
        walls[0][0][1] = 0  # Remove east wall of (0,0)
        walls[0][1][1] = 0  # Remove east wall of (0,1)
        walls[0][2][1] = 0  # Remove east wall of (0,2)
        walls[0][3][0] = 0  # Remove north wall of (0,3)
        walls[1][2][0] = 0  # Remove north wall of (1,2)
        walls[1][3][0] = 0  # Remove north wall of (1,3)
        walls[2][2][3] = 0  # Remove west wall of (2,2)
        walls[2][3][0] = 0  # Remove north wall of (2,3)
        walls[2][1][2] = 0  # Remove south wall of (2,1)
        walls[1][1][1] = 0  # Remove east wall of (1,1)

        # Make sure the center is accessible
        walls[1][1][0] = 0  # Remove north wall between (1,1) and (2,1)
        walls[1][2][1] = 0  # Remove east wall between (1,2) and (1,3)

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_4x4_simple_maze(self) -> List[List[List[int]]]:
        """Create a simpler 4x4 maze with a direct path to the center."""
        size = 4
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Remove south wall at the start
        walls[0][0][2] = 0  

        # Create a direct path to the center
        walls[0][0][1] = 0  # Remove east wall of (0,0)
        walls[0][1][0] = 0  # Remove north wall of (0,1)
        walls[1][1][1] = 0  # Remove east wall of (1,1)
        walls[1][2][1] = 0  # Remove east wall of (1,2)

        # Ensure center cells are interconnected
        walls[1][1][0] = 0  # Remove north wall of (1,1)
        walls[1][2][0] = 0  # Remove north wall of (1,2)

        # Add a few more paths for exploration
        walls[2][0][1] = 0  # Remove east wall of (2,0)
        walls[3][1][2] = 0  # Remove south wall of (3,1)

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_4x4_complex_maze(self) -> List[List[List[int]]]:
        """Create a more complex 4x4 maze with multiple paths and some dead ends."""
        size = 4
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Remove south wall at the start
        walls[0][0][2] = 0  

        # Create a winding path with dead ends
        walls[0][0][1] = 0  # Remove east wall of (0,0)
        walls[0][1][0] = 0  # Remove north wall of (0,1)
        walls[1][1][3] = 0  # Remove west wall of (1,1)
        walls[1][0][0] = 0  # Remove north wall of (1,0)
        walls[2][0][1] = 0  # Remove east wall of (2,0)
        walls[2][1][1] = 0  # Remove east wall of (2,1)

        # Create a loop around the center
        walls[1][2][0] = 0  # Remove north wall of (1,2)
        walls[2][2][1] = 0  # Remove east wall of (2,2)
        walls[2][3][2] = 0  # Remove south wall of (2,3)
        walls[1][3][3] = 0  # Remove west wall of (1,3)

        # Connect to center cells
        walls[2][1][0] = 0  # Remove north wall of (2,1)
        walls[2][2][2] = 0  # Remove south wall of (2,2)

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_16x16_classic_maze(self) -> List[List[List[int]]]:
        """Create a standard 16x16 maze with a clear path to the center."""
        size = 16
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Create entrance at bottom left
        walls[0][0][2] = 0  # Remove south wall of (0,0)

        # Create a main path to the center
        current_x, current_y = 0, 0
        target_x, target_y = size // 2 - 1, size // 2 - 1  # Center of the maze

        # Simple algorithm to create a path to the center
        while not (current_x == target_x and current_y == target_y):
            # Decide direction (prefer moving toward the center)
            if current_x < target_x and random.random() < 0.7:  # Move east
                walls[current_y][current_x][1] = 0  # Remove east wall
                current_x += 1
            elif current_x > target_x and random.random() < 0.7:  # Move west
                walls[current_y][current_x][3] = 0  # Remove west wall
                current_x -= 1
            elif current_y < target_y and random.random() < 0.7:  # Move north
                walls[current_y][current_x][0] = 0  # Remove north wall
                current_y += 1
            elif current_y > target_y:  # Move south
                walls[current_y][current_x][2] = 0  # Remove south wall
                current_y -= 1
            else:  # Random move if not advancing toward center
                direction = random.randint(0, 3)
                if direction == 0 and current_y < size - 1:  # North
                    walls[current_y][current_x][0] = 0
                    current_y += 1
                elif direction == 1 and current_x < size - 1:  # East
                    walls[current_y][current_x][1] = 0
                    current_x += 1
                elif direction == 2 and current_y > 0:  # South
                    walls[current_y][current_x][2] = 0
                    current_y -= 1
                elif direction == 3 and current_x > 0:  # West
                    walls[current_y][current_x][3] = 0
                    current_x -= 1

        # Make center a 2x2 open area
        center_x, center_y = size // 2 - 1, size // 2 - 1

        # Connect center cells (remove internal walls)
        for y in range(center_y, center_y + 2):
            for x in range(center_x, center_x + 2):
                if x < center_x + 1:  # Not the rightmost cell
                    walls[y][x][1] = 0  # Remove east wall
                if y < center_y + 1:  # Not the topmost cell
                    walls[y][x][0] = 0  # Remove north wall

        # Add some random paths throughout the maze
        for _ in range(size * 3):  # Add a number of random connections
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            direction = random.randint(0, 3)

            if direction == 0 and y < size - 1:  # North
                walls[y][x][0] = 0
            elif direction == 1 and x < size - 1:  # East
                walls[y][x][1] = 0
            elif direction == 2 and y > 0:  # South
                walls[y][x][2] = 0
            elif direction == 3 and x > 0:  # West
                walls[y][x][3] = 0

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_16x16_random_maze(self) -> List[List[List[int]]]:
        """Create a completely random 16x16 maze using a depth-first search algorithm."""
        size = 16
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Initialize visited cells grid
        visited = [[False for _ in range(size)] for _ in range(size)]

        # Create entrance at bottom left
        walls[0][0][2] = 0  # Remove south wall of (0,0)

        # Depth-first search maze generation
        stack = [(0, 0)]  # Start at the bottom-left cell
        visited[0][0] = True

        while stack:
            x, y = stack[-1]  # Current cell at the top of the stack

            # Get unvisited neighbors
            neighbors = []
            if y > 0 and not visited[y-1][x]:  # South
                neighbors.append((x, y-1, 2, 0))  # (x, y, direction, opposite_direction)
            if x < size - 1 and not visited[y][x+1]:  # East
                neighbors.append((x+1, y, 1, 3))
            if y < size - 1 and not visited[y+1][x]:  # North
                neighbors.append((x, y+1, 0, 2))
            if x > 0 and not visited[y][x-1]:  # West
                neighbors.append((x-1, y, 3, 1))

            if neighbors:
                # Choose a random unvisited neighbor
                next_x, next_y, direction, opposite = random.choice(neighbors)

                # Remove the wall between the current cell and the chosen neighbor
                walls[y][x][direction] = 0
                walls[next_y][next_x][opposite] = 0

                # Mark the neighbor as visited and add it to the stack
                visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                # Backtrack if no unvisited neighbors
                stack.pop()

        # Make center a 2x2 open area
        center_x, center_y = size // 2 - 1, size // 2 - 1

        # Connect center cells (remove internal walls)
        for y in range(center_y, center_y + 2):
            for x in range(center_x, center_x + 2):
                if x < center_x + 1:  # Not the rightmost cell
                    walls[y][x][1] = 0  # Remove east wall
                    walls[y][x+1][3] = 0  # Remove west wall of adjacent cell
                if y < center_y + 1:  # Not the topmost cell
                    walls[y][x][0] = 0  # Remove north wall
                    walls[y+1][x][2] = 0  # Remove south wall of adjacent cell

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_16x16_competition_maze(self) -> List[List[List[int]]]:
        """Create a 16x16 maze that mimics standard micromouse competition layouts."""
        size = 16
        # Initialize with all walls
        walls = [[[1, 1, 1, 1] for _ in range(size)] for _ in range(size)]

        # Create entrance at bottom left
        walls[0][0][2] = 0  # Remove south wall of (0,0)

        # In competition mazes, there are often multiple possible paths to the center
        # with the optimal path requiring careful planning

        # First, create a spanning tree maze (to ensure the maze is fully connected)
        self._create_spanning_tree_maze(walls, size)

        # Define the center area (4x4 in the middle)
        center_start_x, center_start_y = size // 2 - 2, size // 2 - 2

        # Make the center area more accessible but still challenging
        # Create multiple entrances to the center region
        entrances = [
            (center_start_x - 1, center_start_y + 1, 1),      # West entrance
            (center_start_x + 1, center_start_y - 1, 0),      # South entrance
            (center_start_x + 4, center_start_y + 2, 3),      # East entrance
            (center_start_x + 2, center_start_y + 4, 2)       # North entrance
        ]

        for x, y, direction in entrances:
            if 0 <= x < size and 0 <= y < size:
                walls[y][x][direction] = 0
                # Update the adjacent cell's wall too for consistency
                nx, ny = x, y
                if direction == 0:  # North
                    ny += 1
                    opposite = 2
                elif direction == 1:  # East
                    nx += 1
                    opposite = 3
                elif direction == 2:  # South
                    ny -= 1
                    opposite = 0
                elif direction == 3:  # West
                    nx -= 1
                    opposite = 1
                
                if 0 <= nx < size and 0 <= ny < size:
                    walls[ny][nx][opposite] = 0

        # Make the center a 2x2 open area
        center_x, center_y = size // 2 - 1, size // 2 - 1
        for y in range(center_y, center_y + 2):
            for x in range(center_x, center_x + 2):
                if x < center_x + 1:
                    walls[y][x][1] = 0
                if y < center_y + 1:
                    walls[y][x][0] = 0

        # Add some loops to provide alternative paths
        # This makes the maze more interesting by adding multiple solution paths
        for _ in range(size):
            x = random.randint(0, size - 2)
            y = random.randint(0, size - 2)

            # Choose between removing a horizontal or vertical wall
            if random.random() < 0.5:
                walls[y][x][1] = 0  # Remove east wall
                walls[y][x+1][3] = 0  # Remove west wall of adjacent cell
            else:
                walls[y][x][0] = 0  # Remove north wall
                walls[y+1][x][2] = 0  # Remove south wall of adjacent cell

        # Add more complex paths closer to the center
        center_region = range(size // 4, 3 * size // 4)
        for _ in range(size * 2):
            x = random.choice(list(center_region))
            y = random.choice(list(center_region))
            direction = random.randint(0, 3)

            if direction == 0 and y < size - 1:  # North
                walls[y][x][0] = 0
                walls[y+1][x][2] = 0
            elif direction == 1 and x < size - 1:  # East
                walls[y][x][1] = 0
                walls[y][x+1][3] = 0
            elif direction == 2 and y > 0:  # South
                walls[y][x][2] = 0
                walls[y-1][x][0] = 0
            elif direction == 3 and x > 0:  # West
                walls[y][x][3] = 0
                walls[y][x-1][1] = 0

        # Ensure consistency of walls between adjacent cells
        self._ensure_wall_consistency(walls, size)

        return walls

    def _create_spanning_tree_maze(self, walls: List[List[List[int]]], size: int) -> None:
        """Helper method to create a spanning tree maze (no loops)."""
        # Track visited cells
        visited = [[False for _ in range(size)] for _ in range(size)]

        # Start at a random cell
        x, y = 0, 0
        visited[y][x] = True

        # Cell stack for backtracking
        stack = [(x, y)]

        # Continue until all cells are visited
        while stack:
            x, y = stack[-1]

            # Find unvisited neighbors
            neighbors = []
            if y > 0 and not visited[y-1][x]:  # South
                neighbors.append((x, y-1, 2, 0))
            if x < size - 1 and not visited[y][x+1]:  # East
                neighbors.append((x+1, y, 1, 3))
            if y < size - 1 and not visited[y+1][x]:  # North
                neighbors.append((x, y+1, 0, 2))
            if x > 0 and not visited[y][x-1]:  # West
                neighbors.append((x-1, y, 3, 1))

            if neighbors:
                # Choose a random unvisited neighbor
                nx, ny, dir_from, dir_to = random.choice(neighbors)

                # Remove walls between cells
                walls[y][x][dir_from] = 0
                walls[ny][nx][dir_to] = 0

                # Mark as visited and add to stack
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                # Backtrack if no unvisited neighbors
                stack.pop()

    def _ensure_wall_consistency(self, walls: List[List[List[int]]], size: int) -> None:
        """Ensure consistency of walls between adjacent cells."""
        for y in range(size):
            for x in range(size):
                # North wall consistency
                if y < size-1 and walls[y][x][0] == 0:
                    walls[y+1][x][2] = 0  # South wall of cell above

                # East wall consistency
                if x < size-1 and walls[y][x][1] == 0:
                    walls[y][x+1][3] = 0  # West wall of cell to the right

                # South wall consistency
                if y > 0 and walls[y][x][2] == 0:
                    walls[y-1][x][0] = 0  # North wall of cell below

                # West wall consistency
                if x > 0 and walls[y][x][3] == 0:
                    walls[y][x-1][1] = 0  # East wall of cell to the left

    def list_available_layouts(self, size: Optional[int] = None) -> Dict[int, List[str]]:
        """List all available maze layouts, optionally filtered by size."""
        if size is not None:
            if size not in self.available_layouts:
                return {}
            return {size: self.available_layouts[size]}
        return self.available_layouts

    def get_center_cells(self, size: int) -> List[Tuple[int, int]]:
        """Returns the coordinates of center cells for a given maze size."""
        if size == 4:
            # For 4x4 maze, center is a 2x2 area at coordinates (1,1), (1,2), (2,1), (2,2)
            return [(1, 1), (1, 2), (2, 1), (2, 2)]
        elif size == 16:
            # For 16x16 maze, center is a 2x2 area at coordinates (7,7), (7,8), (8,7), (8,8)
            return [(7, 7), (7, 8), (8, 7), (8, 8)]
        else:
            raise ValueError(f"Unsupported maze size: {size}")


# Example usage
if __name__ == "__main__":
    # Create a maze generator
    generator = MazeGenerator()

    # Generate a 4x4 maze with the default layout
    maze_4x4 = generator.generate_maze(4, "default")

    # Generate a 16x16 maze with the competition layout
    maze_16x16 = generator.generate_maze(16, "competition")

    # Print available layouts
    print("Available layouts:", generator.list_available_layouts())

    # Print the center cells for a 16x16 maze
    print("Center cells for 16x16 maze:", generator.get_center_cells(16))