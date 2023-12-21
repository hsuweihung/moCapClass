int inAPin = 9;  // Pin for INA
int inBPin = 10; // Pin for INB

void setup() {
  Serial.begin(9600);
  pinMode(inAPin, OUTPUT);
  pinMode(inBPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case '0': // Stop
        analogWrite(inAPin, 0);
        analogWrite(inBPin, 0);
        break;
      case '1': // Speed 1
        analogWrite(inAPin, 70); // PWM Value
        analogWrite(inBPin, 0);
        break;
      case '2': // Speed 2
        analogWrite(inAPin, 110); // PWM Value
        analogWrite(inBPin, 0);
        break;
      case '3': // Speed 3
        analogWrite(inAPin, 160); // PWM Value
        analogWrite(inBPin, 0);
        break;
      case '4': // Speed 4
        analogWrite(inAPin, 210); // PWM Value
        analogWrite(inBPin, 0);
        break;
      case '5': // Speed 5
        analogWrite(inAPin, 255); // PWM Value
        analogWrite(inBPin, 0);
        break;
      default:
        analogWrite(inAPin, 0);
        analogWrite(inBPin, 0);
        break;
    }
  }
}
