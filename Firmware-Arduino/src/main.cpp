#include <Arduino.h>

#include "config.h"
#include "leds.h"
#include "statemachines.h"
#include "trains.h"
#include "wifi.h"
#include "sleep.h"


void setup() {
  Serial.begin(9600);
  InitDisplay();
  InitTrains();
  InitWiFi();
  ResetSleep();
}

void loop() {
  ExecStatemachines();
  CheckWiFi();
  CheckSleep();
}
