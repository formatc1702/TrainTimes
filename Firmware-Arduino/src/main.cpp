#include <Arduino.h>

#include "config.h"
#include "leds.h"
#include "statemachines.h"


void setup() {
  Serial.begin(9600);
  InitDisplay();
}

void loop() {
  ExecLedSM();
}
