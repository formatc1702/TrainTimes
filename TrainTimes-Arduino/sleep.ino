#include "LowPower.h"

#define SLEEP_DELAY 20000

void CheckSleep() {
  if (millis() > SLEEP_DELAY)
    GoToSleep();
}

void GoToSleep() {
  SleepDisplays();
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
}

