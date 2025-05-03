#include <Wire.h> 
#include <LiquidCrystal_I2C.h> // LiquidCrystal I2C@1.1.2 from Library Manager
#include <EEPROM.h> // for persistent memory

// The Arduino Mega's 4kb (4096 bytes) EEPROM memory is not erased when powered off.

// RESOURCES:
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.33_ultrasonic_module.html#ar-ultrasonic
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.13_motor.html#ar-motor 
//

/*
 *   For a 4x4 maze, assume we enter cell zero (0) in the bottom-left from the South (initial heading is North).
 *   The center will always be cells 5, 6, 9, & 10.
 *
 *    .____ ____ ____ ____.
 *    | 12 | 13 | 14 | 15 |
 *    |  8 |  9 | 10 | 11 |
 *    |  4 |  5 |  6 |  7 |
 *    |  0 |  1 |  2 |  3 |
 *    .     ____ ____ ____.
 *       ^
 *.      |
 *     Enter
 *
 */

const int echoPin = 4;
const int trigPin = 5;
const int motor1A = 10;
const int motor2A = 9;

int loopCount = 0;

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27,16,2);

// Maze search variables
byte heading = 0;         // 0=North, 1=East, 2=South, 3=West
int cell = -1;            // [0:15] for a 4x4 maze, initialize with -1 when starting outside of the maze
int pathHistory[] = {0};  // Array for path history in Search, might help with decision making
int MAZE_SIZE = 4;        // Future work to enable dynamic maze sizes

// Cell structure for Micromouse maze memory
// Total size: 3 bytes per cell
struct MazeCell {
  // Wall information - 1 byte
  // Bit representation for walls (2 bits per wall direction):
  // 00 = known to be open
  // 01 = known to have wall
  // 10 = unknown (not yet observed)
  // Bits 0-1: North wall
  // Bits 2-3: East wall
  // Bits 4-5: South wall
  // Bits 6-7: West wall
  byte wallInfo;

  // Visited flag - 1 bit (packed into a byte for simplicity)
  // 0 = unvisited, 1 = visited
  byte visited;

  // Distance value - 1 byte
  // 0-254: Distance from center
  // 255: Uninitialized
  byte distance;
};

void setup() {
  // put your setup code here, to run once

  // initialize the motor
  pinMode(motor1A, OUTPUT);
  pinMode(motor2A, OUTPUT);

  // initialize the LCD
  lcd.init();
  lcd.backlight();

  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.println("\n\nNow setting up Micromouse...\n\n");

  lcd.setCursor(2, 0);
  lcd.print("Micromouse!");
  lcd.setCursor(2, 1);
  lcd.print("- by Chris J");
}

void loop() {
  // put your main code here, to run repeatedly

  // Micromouse Search:
  // - Move forward to the next cell (and update current cell)
  // - Check ultrasound distance, is there a wall in front of us?
  // - Update knowledge about the current cell in EEPROM
  // - If no wall in front of us, FIN
  // - Turn right (and update heading)
  // - Check ultrasound distance, is there a wall in front of us?
  // - Update knowledge about the current cell in EEPROM
  // - If no wall in front of us, FIN
  // - Turn around (180°)
  // - Check ultrasound distance, is there a wall in front of us?
  // - Update knowledge about the current cell in EEPROM
  // - If no wall in front of us, FIN
  // - Turn left, FIN

  DCmotor_stopMotor();

  if (loopCount == 0) {
    Serial.println("First loop. Clearing LCD in 3 seconds.");
    delay(2900);
    //lcd.clear();
    loopCount = 1;
    lcd.setCursor(2, 0);
    delay(100);
  }
  //lcd_print_loop();
  //lcd.setCursor(2, 0);
  //lcd.print("Running...");

  moveForward();

  float distance = readSensorData();
  bool wallDetected;
  wallDetected = isThereAWallInFrontOfMe(distance);

  /*
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    switch (incomingByte) {
      case 'A':
        DCmotor_clockwise(255);
        Serial.println("The motor rotate clockwise.");
        break;
      case 'B':
        DCmotor_anticlockwise(255);
        Serial.println("The motor rotate anticlockwise.");
        break;
    }
  }
  */

  delay(200);
  //delay(3000);

  // Check if we're in the center to end search mode
  if (isAtCenter()) {
    Serial.println("Found the center!");

    // TODO Beep or something to alert us :)

    // Chill until the robot is picked up and reset
    while(1) {delay(1000);}
  }

  if(wallDetected) {
    // Turn right and check again
    turnRight();
    float rightDistance = readSensorData();
    bool rightWallDetected;
    rightWallDetected = isThereAWallInFrontOfMe(rightDistance);
  }
}

float readSensorData(){
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);  
  float distance = pulseIn(echoPin, HIGH)/58.00;  //Equivalent to (340m/s*1us)/2
  return distance;
}

bool moveForward() {
  return true;
}

// Update heading when turning right (90° clockwise)
void turnRight() {
  heading = (heading + 1) % 4;
  // 0->1, 1->2, 2->3, 3->0
}

// Update heading when turning left (90° counterclockwise)
void turnLeft() {
  heading = (heading + 3) % 4;
  // 0->3, 1->0, 2->1, 3->2
  // Using (heading + 3) % 4 is equivalent to (heading - 1) % 4
  // but avoids negative numbers
}

// Update heading when turning around (180°)
void turnAround() {
  heading = (heading + 2) % 4;
  // 0->2, 1->3, 2->0, 3->1
}

void DCmotor_clockwise(int Speed)
{
  analogWrite(motor1A, 0);
  analogWrite(motor2A, Speed);
}

void DCmotor_anticlockwise(int Speed)
{
  analogWrite(motor1A, Speed);
  analogWrite(motor2A, 0);
}

void DCmotor_stopMotor()
{
  analogWrite(motor1A, 0);
  analogWrite(motor2A, 0);
}

void lcd_print_loop() {
  Serial.println("Inside the LCD Print Loop.");
  //lcd.clear();
  lcd.setCursor(2, 0); // Set cursor at position three(3) on first line of 1602 LCD
  char dash = '-';
  for (int i = 0; i <= 9; i++) {
    //lcd.print(i); // Display succesive values of variable i
    lcd.print(dash);
    delay(100); // Delay after each display of i
  }
}

// Check ultrasound distance, is there a wall in front of us?
// Also, update knowledge about the current cell in EEPROM
bool isThereAWallInFrontOfMe(int distance) {
  Serial.print(distance);
  Serial.println(" cm.  <-- ultrasonic sensor reading");

  if (distance < 10.0) {
    DCmotor_stopMotor();
    Serial.println("Obstacle detected. Stopping!");
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("obstacle!");
    delay(800);
    recordWallInfo(true);
    return true;
  }
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("Running...");
  delay(10);
  recordWallInfo(false);
  return false;
}

// Example function to set wall information for a given cell
void setWall(byte &wallInfo, byte direction, byte value) {
  // direction: 0=North, 1=East, 2=South, 3=West
  // value: 0=open, 1=wall, 2=unknown
  byte shift = direction * 2;
  // Clear the bits at the position
  wallInfo &= ~(0b11 << shift);
  // Set the new value
  wallInfo |= (value & 0b11) << shift;
}

// Example function to get wall information for a given cell
byte getWall(byte wallInfo, byte direction) {
  // direction: 0=North, 1=East, 2=South, 3=West
  // returns: 0=open, 1=wall, 2=unknown
  byte shift = direction * 2;
  return (wallInfo >> shift) & 0b11;
}

// Check if current cell is one of the target center cells
bool isAtCenter() {
  return (cell == 5 || cell == 6 || cell == 9 || cell == 10);
}

// Update cell position when moving forward based on current heading
// Returns true if move is valid, false if it would go outside maze
bool updateCellPosition() {
  int newCell = cell;

  switch (heading) {
    case 0: // North
      newCell = cell + 4;
      break;
    case 1: // East
      newCell = cell + 1;
      break;
    case 2: // South
      newCell = cell - 4;
      break;
    case 3: // West
      newCell = cell - 1;
      break;
  }

  // Check if new position is valid (within 4x4 maze)
  if (newCell < 0 || newCell > 15) {
    return false; // Outside maze boundaries
  }

  // Check for invalid edge transitions (wrapping around edges)
  if ((cell % 4 == 3 && newCell % 4 == 0) || // Right edge to left edge
      (cell % 4 == 0 && newCell % 4 == 3)) { // Left edge to right edge
    return false;
  }

  // Valid move, update cell position
  cell = newCell;

  // Update path history (assuming pathHistory is implemented elsewhere)
  // This is simplified - you would need proper path history management
  updatePathHistory(cell);

  return true;
}

void recordWallInfo(bool wallDetected) {
  // Skip if we're not in a valid cell
  if (cell < 0 || cell > 15) return;

  // Read current cell data from EEPROM
  int eepromAddr = cell * sizeof(MazeCell);
  MazeCell currentCell;
  EEPROM.get(eepromAddr, currentCell);

  // Determine which wall we're facing based on our heading
  byte wallDirection = heading; // 0=North, 1=East, 2=South, 3=West

  // Set the wall information (0=open, 1=wall, 2=unknown)
  byte wallValue = wallDetected ? 1 : 0;
  setWall(currentCell.wallInfo, wallDirection, wallValue);

  // Mark cell as visited
  currentCell.visited = 1;

  // Write updated data back to EEPROM
  EEPROM.put(eepromAddr, currentCell);

  // Debug output
  /*
  Serial.print("Updated cell ");
  Serial.print(cell);
  Serial.print(" wall info: ");
  Serial.println(currentCell.wallInfo, BIN);
  */

  // Update the corresponding wall in the adjacent cell (if it exists)
  int adjacentCell = -1;
  byte oppositeWall = (wallDirection + 2) % 4; // Calculate opposite wall direction

  // Calculate adjacent cell based on current heading
  switch (heading) {
    case 0: // North
      adjacentCell = cell + 4;
      break;
    case 1: // East
      adjacentCell = cell + 1;
      break;
    case 2: // South
      adjacentCell = cell - 4;
      break;
    case 3: // West
      adjacentCell = cell - 1;
      break;
  }

  // Check if adjacent cell is valid (within maze boundaries)
  if (adjacentCell >= 0 && adjacentCell < 16) {
    // Check for invalid edge transitions (e.g. wrapping around from right edge to left edge)
    bool invalidEdge = false;
    if ((cell % 4 == 3 && adjacentCell % 4 == 0) || // Right edge to left edge
        (cell % 4 == 0 && adjacentCell % 4 == 3)) { // Left edge to right edge
      invalidEdge = true;
    }

    if (!invalidEdge) {
      // Read adjacent cell data
      int adjacentAddr = adjacentCell * sizeof(MazeCell);
      MazeCell adjacentCellData;
      EEPROM.get(adjacentAddr, adjacentCellData);

      // Update the opposite wall in the adjacent cell
      setWall(adjacentCellData.wallInfo, oppositeWall, wallValue);

      // Write updated data back to EEPROM
      EEPROM.put(adjacentAddr, adjacentCellData);

      Serial.print("Updated adjacent cell ");
      Serial.print(adjacentCell);
      Serial.print(" wall info: ");
      Serial.println(adjacentCellData.wallInfo, BIN);
    }
  }
}

// Helper function to update path history
void updatePathHistory(int newCell) {
  // This is a placeholder - you would need to implement proper path history management
  // For example, adding the new cell to the history array
  // pathHistory[pathHistoryIndex++] = newCell;
}

// Clear the entire EEPROM memory
void EEPROM_clear() {
  for (int i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.write(i, 0);
  }
}

// Initialize the maze with known outer walls and unknown interior walls
void initializeMaze() {
  Serial.println("Initializing maze in EEPROM...");

  // Loop through all cells in the 4x4 maze
  for (int cellIdx = 0; cellIdx < 16; cellIdx++) {
    MazeCell cell;

    // Set all walls initially to unknown (value 2)
    cell.wallInfo = 0;
    for (int dir = 0; dir < 4; dir++) {
      setWall(cell.wallInfo, dir, 2); // 2 = unknown
    }

    // Check if this cell is on any edge and set outer walls accordingly

    // North edge (top row: cells 12-15)
    if (cellIdx >= 12 && cellIdx <= 15) {
      setWall(cell.wallInfo, 0, 1); // North wall exists
    }

    // East edge (rightmost column: cells 3, 7, 11, 15)
    if (cellIdx % 4 == 3) {
      setWall(cell.wallInfo, 1, 1); // East wall exists
    }

    // South edge (bottom row: cells 0-3)
    if (cellIdx >= 0 && cellIdx <= 3) {
      setWall(cell.wallInfo, 2, 1); // South wall exists
    }

    // West edge (leftmost column: cells 0, 4, 8, 12)
    if (cellIdx % 4 == 0) {
      setWall(cell.wallInfo, 3, 1); // West wall exists
    }

    // Mark all cells as unvisited
    cell.visited = 0;

    // Set distance values - 255 for uninitialized
    cell.distance = 255;

    // Set center cells with initial distance of 0
    if (cellIdx == 5 || cellIdx == 6 || cellIdx == 9 || cellIdx == 10) {
      cell.distance = 0; // Center cells
    }

    // Write the initialized cell to EEPROM
    int eepromAddr = cellIdx * sizeof(MazeCell);
    EEPROM.put(eepromAddr, cell);
  }

  // Special case for the entry point (we'll enter from south of cell 0)
  // Open the south wall of cell 0 (this would be our entry point)
  int entryCell = 0;
  int entryAddr = entryCell * sizeof(MazeCell);
  MazeCell entryData;
  EEPROM.get(entryAddr, entryData);
  setWall(entryData.wallInfo, 2, 0); // 0 = open (south wall of cell 0)
  EEPROM.put(entryAddr, entryData);

  Serial.println("Maze initialization complete!");

  // Debug: print initialized maze wall information
  Serial.println("Initialized maze wall information:");
  for (int i = 0; i < 16; i++) {
    MazeCell debugCell;
    EEPROM.get(i * sizeof(MazeCell), debugCell);
    Serial.print("Cell ");
    Serial.print(i);
    Serial.print(": Wall info = ");
    Serial.print(debugCell.wallInfo, BIN);
    Serial.print(", Distance = ");
    Serial.println(debugCell.distance);
  }
}