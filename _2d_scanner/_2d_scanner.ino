/**
 * Base code for Arduino.
 */

#include <Stepper.h>

// Globals
#define BAUDRATE 9600
#define NUM_POLLS 10

#define SCAN_SPEED 60
#define X_SCAN_STEPS 300
#define X_SCAN_INTERVAL 5
#define Y_SCAN_STEPS 700
#define Y_SCAN_INTERVAL 1

Stepper x_motor(512, 4, 6, 5, 7);
Stepper y_motor(512, 8, 10, 9, 11);

char* tmp;

void setup() {
  Serial.begin(BAUDRATE);

  for (int i = 4; i < 12; ++i) {
    pinMode(i, OUTPUT);
  }

  x_motor.setSpeed(SCAN_SPEED);
  y_motor.setSpeed(SCAN_SPEED);
}

void loop() {
  String data = Serial.readString();
  float value_sum = 0;
  if (data == "begin") {
    Serial.println("start");
    Serial.println("{ 'type': '2d' }");
    sprintf(tmp, "{ 'width': '%d' }", X_SCAN_STEPS);
    Serial.println(tmp);
    sprintf(tmp, "{ 'height': '%d' }", Y_SCAN_STEPS);
    Serial.println(tmp);
    for (int y = 0; y < Y_SCAN_STEPS; ++y) {
      for (int x = 0; x < X_SCAN_STEPS; ++x) {
        value_sum = 0;
        for (int i = 0; i < NUM_POLLS; ++i) {
          value_sum += analogRead(A0);
          delay(2);
        }
        Serial.println(value_sum / 10.0);
        x_motor.step(X_SCAN_INTERVAL);
      }
      x_motor.step(-X_SCAN_INTERVAL * X_SCAN_STEPS);
      y_motor.step(Y_SCAN_INTERVAL);
    }
    Serial.println("end");
    y_motor.step(-5 * Y_SCAN_STEPS);
  }
}

