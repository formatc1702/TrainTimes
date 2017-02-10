

#include <SoftwareSerial.h>

#define PIN_ESP_CHPD 3

SoftwareSerial wifi(4,2);
//#define wifi Serial  // DEBUG ONLY!!!

//String WiFiString;

void WiFiInit() {
  pinMode     (PIN_ESP_CHPD, OUTPUT);
  digitalWrite(PIN_ESP_CHPD, LOW);
  delay(100);
  digitalWrite(PIN_ESP_CHPD, HIGH);
  pinMode     (PIN_ESP_CHPD, INPUT);
  
  wifi.begin(9600);
  wifi.setTimeout(50);
//  WiFiString = "";
}
