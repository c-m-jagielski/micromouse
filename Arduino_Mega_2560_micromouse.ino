#include <Wire.h> 
#include <LiquidCrystal_I2C.h> // LiquidCrystal I2C@1.1.2 from Library Manager

// The 4kb (4096 bytes) EEPROM memory is not erased when powered off.

// RESOURCES:
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.33_ultrasonic_module.html#ar-ultrasonic
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.13_motor.html#ar-motor 

const int echoPin = 4;
const int trigPin = 5;
const int motor1A = 10;
const int motor2A = 9;

// set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27,16,2);

void setup() {
  // put your setup code here, to run once:

  // initialize the motor
  pinMode(motor1A, OUTPUT);
  pinMode(motor2A, OUTPUT);

  // initialize the LCD
  lcd.init();
  lcd.backlight();

  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.println("Hi there!");
  Serial.println("Ultrasonic sensor.");
  
  lcd.setCursor(2, 0);
  lcd.print("Micromouse!");
  lcd.setCursor(2, 1);
  lcd.print("- by Chris J");
}

void loop() { }
void blah() {
  // put your main code here, to run repeatedly:

  //lcd.clear();

  float distance = readSensorData();
  Serial.print(distance);   
  Serial.println(" cm.  <-- ultrasonic sensor reading");

  if (distance < 10.0) {
    stopMotor();
    Serial.println("Obstacle detected. Stopping!");
    //lcd.setCursor(2, 0);
    //lcd.print("obstacle!");
    //lcd.print(88);
    //delay(5000);
  } else { clockwise(255); }

  /*
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    switch (incomingByte) {
      case 'A':
        clockwise(255);
        Serial.println("The motor rotate clockwise.");
        break;
      case 'B':
        anticlockwise(255);
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

void clockwise(int Speed)
{
  analogWrite(motor1A, 0);
  analogWrite(motor2A, Speed);
}

void anticlockwise(int Speed)
{
  analogWrite(motor1A, Speed);
  analogWrite(motor2A, 0);
}

void stopMotor()
{
  analogWrite(motor1A, 0);
  analogWrite(motor2A, 0);
}
