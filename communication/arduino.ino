#include <Stepper.h>
#include <Servo.h>
#include <SoftwareSerial.h>

Servo servo; 
SoftwareSerial soft(2,3);

int value_A0, value_A1;
int stepSize=22.22222; //stepper모터에 달린 기어 1칸당 40도 이동. 40/steps=22.2222


const int stepsPerRevolution = 200;  // 
//  360/1.8=200 -> 1에 1.8도

Stepper myStepper(stepsPerRevolution, 3, 4, 5, 6);


void setup() {
  Serial.begin(9600);
  soft.begin(9600);
  myStepper.setSpeed(60); //rpm 30
  servo.attach(9);

}

void loop() {
  if(soft.available()) {
    float rot;
    String dir = soft.readStringUntil('\n');
    
    String receivedNumber = soft.readStringUntil('\n');
    
    if (receivedNumber.toInt() != 0) {
      if (dir.toInt() == 1) {
        Serial.println("Direction: Right");
        rot = receivedNumber.toInt() * stepSize;
        Serial.print("Received: ");
        Serial.println(receivedNumber.toInt());

        servo.write(40);
        delay(1000);
        myStepper.step(rot);
        delay(1000);
        servo.write(120);
        delay(1000);
      } 
      else {
        Serial.println("Direction: Left");
        rot = -1 * receivedNumber.toInt() * stepSize;
        Serial.print("Received: ");
        Serial.println(receivedNumber.toInt());

        servo.write(40);
        delay(1000);
        myStepper.step(rot);
        delay(1000);
        servo.write(120);
        delay(1000);
      }
    } 
  }
  
  value_A0 = digitalRead(A0); //test용 스위치 연결 누르면 LOW
  value_A1 = digitalRead(A1);

  if (value_A0 == LOW){
   
    servo.write(60);
    delay(1000);

    myStepper.step(stepSize);

    servo.write(120);
    delay(1000);
  }

  if (value_A1 == LOW){
   
    servo.write(60);
    delay(1000);

    myStepper.step(-stepSize);

    servo.write(120);
    delay(1000);
  }
  
}//스위치 2개 추가
