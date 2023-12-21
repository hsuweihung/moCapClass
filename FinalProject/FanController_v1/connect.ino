int fanPin = 2;
int fanSpeed = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(fanPin, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0)
  {
    char command = Serial.read();

    if (command == '0')
    {
      analogWrite(fanPin, 0);
    }
    else if (command >= '1' && command <= '3')
    {
      fanSpeed = (command - '0') * 85;
      analogWrite(fanPin, fanSpeed);
    }
  }
}
