#include "wifi.h"
#include <Arduino.h>
#include <SoftwareSerial.h>

#include "config.h"
#include "trains.h"
#include "sleep.h"

#define PIN_ESP_CHPD 3

// SoftwareSerial wifi(4,2);
#define wifi Serial  // DEBUG ONLY!!!

//String WiFiString;

void InitWiFi() {
  // Reset ESP8266 through CHPD (ESP-01) or RST (NodeMCU) pin
  pinMode     (PIN_ESP_CHPD, OUTPUT);
  digitalWrite(PIN_ESP_CHPD, LOW);
  delay(100);
  digitalWrite(PIN_ESP_CHPD, HIGH);
  pinMode     (PIN_ESP_CHPD, INPUT);

  wifi.begin(9600);
  wifi.setTimeout(100);
}

void CheckWiFi() {
  if (wifi.available() > 0) { // something has arrived
    Serial.print(".");
    char buf = wifi.read();
    if (buf == '{') {         // found start character
      boolean valid = true;
      Serial.print("{");
      Serial.println();
      for (EACH_TRAINLINE) {
        for (EACH_DEPARTURE) {
          int newtime = wifi.parseInt();
          if (newtime == 0) {
            valid = false;
            break;
          }
          setTrainTime(line, dep, newtime);
          Serial.print(newtime);
          Serial.print("\t\t");
        }
        Serial.println();
        if (valid == false)
          break;
      }
      if (valid) {
        EnableTrains();
        ResetSleep();
        Serial.print("} OK!");
      } else {
        Serial.print("ERROR");
      }
      Serial.flush();
    }
  }
}
