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
int cell = 0;             // [0:15] for a 4x4 maze
int pathHistory[] = {0};  // Array for path history in Search, might help with decision making

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

  float distance = readSensorData();
  Serial.print(distance);   
  Serial.println(" cm.  <-- ultrasonic sensor reading");

  if (distance < 10.0) {
    DCmotor_stopMotor();
    Serial.println("Obstacle detected. Stopping!");
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("obstacle!");
    delay(800);
  } else {
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("Running...");
    //clockwise(255);
    delay(10);
  }

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
