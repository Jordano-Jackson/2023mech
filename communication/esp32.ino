#include <BluetoothSerial.h>
#include <ESP32Servo.h>
#include <Stepper.h>

BluetoothSerial SerialBT;
Servo servo;

// Step motor setting
const int stepsPerRevolution = 200;
//  360/1.8=200 -> 1에 1.8도
Stepper myStepper(stepsPerRevolution, 14, 27, 16, 25);

const int stepSize = 22.23;

void setup() {
  Serial.begin(9600);
  SerialBT.begin("ESP32"); // Bluetooth 이름 설정
  myStepper.setSpeed(30); //rpm 30

  servo.attach(2);
}

void loop() {
  if (SerialBT.available()) {
    float rot;
    String dir = SerialBT.readStringUntil('\n');
    
    String receivedNumber = SerialBT.readStringUntil('\n');
    
    if (receivedNumber != 0) {
      if (dir.toInt() == 1) {
        Serial.println("Direction: Right");
        rot = receivedNumber.toInt() * stepSize;
      }
      else {
        Serial.println("Direction: Left");
        rot = -1 * receivedNumber.toInt() * stepSize;
      }
      Serial.print("Received: ");
      Serial.print(receivedNumber.toInt());
      Serial.println("");

      servo.write(40);
      delay(500);
      myStepper.step(rot);
      delay(500);
      servo.write(120);
      delay(500);
    } 
  }
}