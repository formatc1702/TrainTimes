#include "sleep.h"

#include "LowPower.h"

#include "leds.h"

#define SLEEP_DELAY 60000

long lastsleepreset = 0;

void CheckSleep() {
  if (millis() - lastsleepreset > SLEEP_DELAY)
    GoToSleep();
}

void ResetSleep() {
  lastsleepreset = millis();
}

void GoToSleep() {
  SleepDisplays();
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
}
