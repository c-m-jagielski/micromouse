// The 4kb (4096 bytes) EEPROM memory is not erased when powered off.

// RESOURCES:
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.33_ultrasonic_module.html#ar-ultrasonic
// https://docs.sunfounder.com/projects/vincent-kit/en/latest/arduino/2.13_motor.html#ar-motor 

const int echoPin = 4;
const int trigPin = 5;
const int motor1A = 10;
const int motor2A = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(motor1A, OUTPUT);
  pinMode(motor2A, OUTPUT);

  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.println("Hi there!");
  Serial.println("Ultrasonic sensor.");
  Serial.println("Please input 'A' or 'B' to select the motor rotate direction.");
}

void loop() {
  // put your main code here, to run repeatedly:

  float distance = readSensorData();
  Serial.print(distance);   
  Serial.println(" cm.  <-- ultrasonic sensor reading");

  if (distance < 10.0) {
    stopMotor();
    Serial.println("Obstacle detected. Stopping!");
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
