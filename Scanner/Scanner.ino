/**
 * Base code for Arduino.
 */

#include <Stepper.h>

// Globals
#define BAUDRATE 9600
#define NUM_POLLS 10

Stepper x_motor(512, 4, 6, 5, 7);
Stepper y_motor(512, 8, 10, 9, 11);

void setup() {
  Serial.begin(BAUDRATE);

  for (int i = 4; i < 12; ++i) {
    pinMode(i, OUTPUT);
  }

  x_motor.setSpeed(30);
  y_motor.setSpeed(30);
}

void loop() {
  float valueSum = 0;
  for (int i = 0; i < NUM_POLLS; ++i) {
    valueSum += analogRead(A0);
    delay(2);
  }
  
  Serial.println(valueSum / 10.0);
  x_motor.step(5);
  y_motor.step(-5);
}
