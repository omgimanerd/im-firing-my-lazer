int values[10];
int index = 0;
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
}

void loop() {
  if(index<10){
      values[index] = analogRead(A0);
      index++;
  }else{
      int total = 0;
      for(index = 0;index<10;index++){
         total+=values[index];
      }
      index = 0;
      Serial.println(total/10);
      delay(100);
  }
  
}
