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

String incoming_message = "";

void setup() {

  Serial.begin(9600);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // startup
  Serial.println("READY");
  Serial.flush();
}

void loop() {
  
  // set the cursor to column 0, line 1
  lcd.setCursor(0, 1);
  
  // receive messages from serial and print them to lcd
  while (Serial.available() > 0){
    incoming_message += char(Serial.read());
    
    if (incoming_message.indexOf("\n") > 0){
      lcd.clear();
      incoming_message.remove(incoming_message.length()-1);
      lcd.print(incoming_message);
      Serial.println(incoming_message);
      incoming_message = "";
    }
  }
}
