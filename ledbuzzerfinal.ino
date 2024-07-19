const int ledPin = 9; 
const int motPin = 8; // Adjust pin number if your LED is connected differently

void setup() {
  Serial.begin(9600);   // Adjust baud rate if necessary (match Python code)
  pinMode(ledPin, OUTPUT);
  pinMode(motPin,OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    digitalWrite(motPin,HIGH);
    if (command == '1') {
      digitalWrite(ledPin, HIGH);
    } else if (command == '0') {
      digitalWrite(ledPin, LOW);
    }
  }

}
