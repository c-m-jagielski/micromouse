// micromouse_wrapper.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cstddef>
#include <cstdio>

namespace py = pybind11;

// Global variables to maintain state
int g_cell = -1;            // Current cell position
int g_heading = 0;          // Current heading: 0=North, 1=East, 2=South, 3=West
bool g_wall_detected = false;  // Flag for wall detection
float g_sensor_reading = 999.0; // Simulated sensor reading

// Structure to represent maze cells (matching your original code)
struct MazeCell {
    unsigned char wallInfo;
    unsigned char visited;
    unsigned char distance;
};

// Vector to store maze cell data
std::vector<MazeCell> g_maze_cells(16);

// Forward declarations of functions from your original code
bool updateCellPosition();
bool isAtCenter();
void recordWallInfo(bool wallDetected);
void turnRight();
void turnLeft();
void turnAround();
void setWall(unsigned char &wallInfo, unsigned char direction, unsigned char value);
unsigned char getWall(unsigned char wallInfo, unsigned char direction);

// Implementations of key functions from your original code
// These are modified to work with our simulated environment

// Update cell position when moving forward based on current heading
bool updateCellPosition() {
    int newCell = g_cell;

    switch (g_heading) {
        case 0: // North
            newCell = g_cell + 4;
            break;
        case 1: // East
            newCell = g_cell + 1;
            break;
        case 2: // South
            newCell = g_cell - 4;
            break;
        case 3: // West
            newCell = g_cell - 1;
            break;
    }

    // Check if new position is valid (within 4x4 maze)
    if (newCell < 0 || newCell > 15) {
        return false; // Outside maze boundaries
    }

    // Check for invalid edge transitions (wrapping around edges)
    if ((g_cell % 4 == 3 && newCell % 4 == 0) || // Right edge to left edge
        (g_cell % 4 == 0 && newCell % 4 == 3)) { // Left edge to right edge
        return false;
    }

    // Valid move, update cell position
    g_cell = newCell;
    
    return true;
}

// Check if current cell is one of the target center cells
bool isAtCenter() {
    return (g_cell == 5 || g_cell == 6 || g_cell == 9 || g_cell == 10);
}

// Update heading when turning right (90° clockwise)
void turnRight() {
    g_heading = (g_heading + 1) % 4;
}

// Update heading when turning left (90° counterclockwise)
void turnLeft() {
    g_heading = (g_heading + 3) % 4;
}

// Update heading when turning around (180°)
void turnAround() {
    g_heading = (g_heading + 2) % 4;
}

// Simulated sensor reading function
float readSensorData() {
    return g_sensor_reading;
}

// Example function to set wall information for a given cell
void setWall(unsigned char &wallInfo, unsigned char direction, unsigned char value) {
    // direction: 0=North, 1=East, 2=South, 3=West
    // value: 0=open, 1=wall, 2=unknown
    unsigned char shift = direction * 2;
    // Clear the bits at the position
    wallInfo &= ~(0b11 << shift);
    // Set the new value
    wallInfo |= (value & 0b11) << shift;
}

// Example function to get wall information for a given cell
unsigned char getWall(unsigned char wallInfo, unsigned char direction) {
    // direction: 0=North, 1=East, 2=South, 3=West
    // returns: 0=open, 1=wall, 2=unknown
    unsigned char shift = direction * 2;
    return (wallInfo >> shift) & 0b11;
}

// Record wall information for the current cell
void recordWallInfo(bool wallDetected) {
    // Skip if we're not in a valid cell
    if (g_cell < 0 || g_cell > 15) return;

    // Get current cell data
    MazeCell& currentCell = g_maze_cells[g_cell];

    // Determine which wall we're facing based on our heading
    unsigned char wallDirection = g_heading; // 0=North, 1=East, 2=South, 3=West

    // Set the wall information (0=open, 1=wall, 2=unknown)
    unsigned char wallValue = wallDetected ? 1 : 0;
    setWall(currentCell.wallInfo, wallDirection, wallValue);

    // Mark cell as visited
    currentCell.visited = 1;

    // Calculate adjacent cell based on current heading
    int adjacentCell = -1;
    unsigned char oppositeWall = (wallDirection + 2) % 4; // Calculate opposite wall direction

    switch (g_heading) {
        case 0: // North
            adjacentCell = g_cell + 4;
            break;
        case 1: // East
            adjacentCell = g_cell + 1;
            break;
        case 2: // South
            adjacentCell = g_cell - 4;
            break;
        case 3: // West
            adjacentCell = g_cell - 1;
            break;
    }

    // Check if adjacent cell is valid (within maze boundaries)
    if (adjacentCell >= 0 && adjacentCell < 16) {
        // Check for invalid edge transitions (e.g. wrapping around from right edge to left edge)
        bool invalidEdge = false;
        if ((g_cell % 4 == 3 && adjacentCell % 4 == 0) || // Right edge to left edge
            (g_cell % 4 == 0 && adjacentCell % 4 == 3)) { // Left edge to right edge
            invalidEdge = true;
        }

        if (!invalidEdge) {
            // Update adjacent cell data
            MazeCell& adjacentCellData = g_maze_cells[adjacentCell];
            
            // Update the opposite wall in the adjacent cell
            setWall(adjacentCellData.wallInfo, oppositeWall, wallValue);
        }
    }
}

// Check for walls and update knowledge
bool isThereAWallInFrontOfMe(float distance) {
    if (distance < 10) {
        std::cout << "Obstacle detected! Distance: " << distance << " cm" << std::endl;
        recordWallInfo(true);
        return true;
    }
    
    recordWallInfo(false);
    return false;
}

// Simulated moveForward function
bool moveForward() {
    return updateCellPosition();
}

// Main algorithm step function - this is what gets called from Python
bool run_step(float sensor_reading) {
    // Store the sensor reading globally
    g_sensor_reading = sensor_reading;
    
    // Check for wall detection
    bool wallDetected = isThereAWallInFrontOfMe(sensor_reading);
    
    // If we've reached the center, return true to signal completion
    if (isAtCenter()) {
        std::cout << "Found the center!" << std::endl;
        return true;
    }
    
    if (wallDetected) {
        // Turn right and check again
        turnRight();
        
        // Simulate checking after turning (in a real implementation, we'd get a new sensor reading)
        float rightDistance = readSensorData();
        bool rightWallDetected = isThereAWallInFrontOfMe(rightDistance);
        
        if (rightWallDetected) {
            // If wall to right, turn around and check
            turnAround();
            
            // Simulate checking after turning
            float backDistance = readSensorData();
            bool backWallDetected = isThereAWallInFrontOfMe(backDistance);
            
            if (backWallDetected) {
                // If wall behind, turn left (we've checked all directions)
                turnLeft();
            }
        }
    }
    else {
        // No wall in front, try moving forward
        moveForward();
    }
    
    return false; // Not done yet
}

// Python module definition
PYBIND11_MODULE(micromouse_cpp, m) {
    m.doc() = "Python bindings for Micromouse C++ code";
    
    // Expose key functions to Python
    m.def("run_step", &run_step, "Run one step of the Micromouse algorithm",
          py::arg("sensor_reading"));
    
    // Functions to get/set the state
    m.def("get_position", []() { return g_cell; }, "Get current cell position");
    m.def("set_position", [](int cell) { g_cell = cell; }, "Set current cell position");
    m.def("get_heading", []() { return g_heading; }, "Get current heading");
    m.def("set_heading", [](int heading) { g_heading = heading; }, "Set current heading");
    
    // Functions to access maze data
    m.def("get_maze_data", []() {
        std::vector<std::map<std::string, int>> result;
        for (size_t i = 0; i < g_maze_cells.size(); i++) {
            std::map<std::string, int> cell_data;
            cell_data["wallInfo"] = g_maze_cells[i].wallInfo;
            cell_data["visited"] = g_maze_cells[i].visited;
            cell_data["distance"] = g_maze_cells[i].distance;
            result.push_back(cell_data);
        }
        return result;
    }, "Get maze cell data");
    
    // Function to initialize the maze
    m.def("initialize_maze", []() {
        for (int i = 0; i < 16; i++) {
            g_maze_cells[i].wallInfo = 0;
            g_maze_cells[i].visited = 0;
            g_maze_cells[i].distance = 255;
            
            // Initialize wall information (all unknown)
            for (int dir = 0; dir < 4; dir++) {
                setWall(g_maze_cells[i].wallInfo, dir, 2); // 2 = unknown
            }
            
            // Set center cells with initial distance of 0
            if (i == 5 || i == 6 || i == 9 || i == 10) {
                g_maze_cells[i].distance = 0; // Center cells
            }
        }
    }, "Initialize maze data");
    
    // Expose navigation functions
    m.def("turn_right", &turnRight, "Turn the mouse right");
    m.def("turn_left", &turnLeft, "Turn the mouse left");
    m.def("turn_around", &turnAround, "Turn the mouse around");
    m.def("move_forward", &moveForward, "Move the mouse forward");
    m.def("is_at_center", &isAtCenter, "Check if the mouse is at the center");
}