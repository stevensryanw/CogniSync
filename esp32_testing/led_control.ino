#include <BluetoothSerial.h>

int LED = 2;
BluetoothSerial SerialBT;

void setup() {
  pinMode(LED, OUTPUT);
  SerialBT.begin("ESP32_LED_Control"); // Bluetooth device name
}

void loop() {
  if (SerialBT.available()) {
    char command = SerialBT.read();
    if (command == 'on') {
      digitalWrite(LED, HIGH);
    } else if (command == 'off') {
      digitalWrite(LED, LOW);
    }
  }
}