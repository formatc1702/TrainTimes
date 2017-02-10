#include <Arduino.h>

#include "config.h"
#include "leds.h"
#include "statemachines.h"
#include "trains.h"


void setup() {
  Serial.begin(9600);
  InitDisplay();
  InitTrains();
}

void loop() {
  ExecStatemachines();
}
