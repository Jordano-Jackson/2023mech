#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);

  SerialBT.begin("ESP32"); // Bluetooth 이름 설정
}

void loop() {
  
  if (SerialBT.available()) {
    float rot;
    String dir = SerialBT.readStringUntil('\n');
    Serial2.println(dir);
    
    String receivedNumber = SerialBT.readStringUntil('\n');
    Serial2.println(receivedNumber);
    Serial.println(receivedNumber);
    
     
  }
}
