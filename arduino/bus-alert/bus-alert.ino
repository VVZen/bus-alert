/*
  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

*/

// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
const int RED_LED = 7, BLUE_LED = 8;

String incoming_message = "";

bool arrival_state = false;

void setup() {

  Serial.begin(9600);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // set up the leds
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  // startup
  Serial.println("READY");
  Serial.flush();
}

void bus_arriving_sequence(bool arrivalState){
  if (arrivalState){
    for (int i = 0; i < 3; i++){
      delay(300);
      digitalWrite(BLUE_LED, HIGH);
      delay(300);
      digitalWrite(BLUE_LED, LOW);
    }
  }
  else {
    digitalWrite(RED_LED, LOW);
  }
}

void loop() {
  
  // set the cursor to column 0, line 1
  lcd.setCursor(0, 1);

  bus_arriving_sequence(arrival_state);
  
  // receive messages from serial and print them to lcd
  while (Serial.available() > 0){
    char current_char = char(Serial.read());
    incoming_message += current_char;

    if (current_char == '#'){
      arrival_state = false;
      incoming_message = "";
    }
    else if (current_char == '^'){
      arrival_state = true;
      incoming_message = "";
    }
    else if (current_char == '-'){
      arrival_state = false;
      incoming_message = "";
      digitalWrite(RED_LED, LOW);
    }
    
    if (incoming_message.indexOf("\n") > 0){
      lcd.clear();
      incoming_message.remove(incoming_message.length()-1);
      lcd.print(incoming_message);
      Serial.println(incoming_message);
      incoming_message = "";
    }
  }
}
