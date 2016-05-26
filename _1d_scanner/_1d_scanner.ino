/**
 * Base code for Arduino.
 */

#include <Stepper.h>

// Globals
#define BAUDRATE 9600
#define NUM_POLLS 10

#define SCAN_SPEED 60
#define SCAN_STEPS 700
#define SCAN_INTERVAL 1

Stepper motor(512, 8, 10, 9, 11);

void setup() {
  Serial.begin(BAUDRATE);
  for (int i = 8; i < 12; ++i) {
    pinMode(i, OUTPUT);
  }
  motor.setSpeed(SCAN_SPEED);
}

void loop() {
  String data = Serial.readString();
  float value_sum = 0;
  Serial.println(data);
  if (data == "begin") {
    Serial.println("start");
    for (int i = 0; i < SCAN_STEPS; ++i) {
      value_sum = 0;
      for (int j = 0; j < NUM_POLLS; ++j) {
        value_sum += analogRead(A0);
        delay(2);
      }
      Serial.println(value_sum / 10.0);
      motor.step(SCAN_INTERVAL);
    }
    Serial.println("end");
    motor.step(-SCAN_INTERVAL * SCAN_STEPS);
  }
}

