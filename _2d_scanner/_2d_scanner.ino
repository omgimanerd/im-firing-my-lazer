/**
 * Base code for Arduino when scanning 2 dimensionally.
 */

#include <Stepper.h>

// Globals
#define BAUDRATE 9600
#define NUM_POLLS 10

// Due to some Arduino voltage bullshit, the scan speed can't go above 45~ or the stepper motors
// won't work. We don't know what the arbitrary upper bound is and we haven't found the reason why
// but it most likely is related to the breakout board controlling the stepper motor.
#define SCAN_SPEED 40
#define X_SCAN_STEPS 15
#define X_SCAN_INTERVAL 25
#define Y_SCAN_STEPS 125
#define Y_SCAN_INTERVAL 50

// The motor drifts some amount every y-iteration. This constant fights against that.
#define DRIFT_CONSTANT -50

Stepper x_motor(512, 4, 6, 5, 7);
Stepper y_motor(512, 8, 10, 9, 11);

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
  Serial.println(data);
  if (data == "begin") {
    Serial.print("{ \"type\": \"2d\", \"width\": ");
    Serial.print(Y_SCAN_STEPS);
    Serial.print(", \"height\": ");
    Serial.print(X_SCAN_STEPS);
    Serial.print(" }\n");
    for (int x = 0; x < X_SCAN_STEPS; ++x) {
      for (int y = 0; y < Y_SCAN_STEPS; ++y) {
        value_sum = 0;
        for (int i = 0; i < NUM_POLLS; ++i) {
          value_sum += analogRead(A0);
          delay(2);
        }
        Serial.println(value_sum / 10.0);
        y_motor.step(Y_SCAN_INTERVAL);
      }
      y_motor.step(-(Y_SCAN_INTERVAL * Y_SCAN_STEPS - DRIFT_CONSTANT));
      x_motor.step(X_SCAN_INTERVAL);
    }
    Serial.println("end");
    x_motor.step(-X_SCAN_INTERVAL * X_SCAN_STEPS);
    y_motor.step(-Y_SCAN_INTERVAL * Y_SCAN_STEPS);
  }
}

