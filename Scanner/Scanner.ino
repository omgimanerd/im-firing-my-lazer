/**
 * Base code for Arduino.
 */

// Globals

void setup() {
  // initialize serial communication at 9600 bits per second
  Serial.begin(9600);  
}

void loop() {
  Serial.println(analogRead(A0));
}