

#include <SoftwareSerial.h>

SoftwareSerial wifi(4,2);

//String WiFiString;

void WiFiInit() {
  wifi.begin(9600);
  wifi.setTimeout(50);
//  WiFiString = "";
}
