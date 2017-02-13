#include "trains.h"
#include <Arduino.h> // max()

#include "config.h"
#include "leds.h" // remove later!
#define RECALC_TIMES_SECONDS 3

int departures      [NUM_TRAINLINES][NUM_DEPARTURETIMES];
int departures_real [NUM_TRAINLINES][NUM_DEPARTURETIMES];
int depshift        [NUM_TRAINLINES];

int timeSinceUpdate = 0;

int trainsready = 0;


void InitTrains() {
  for   (EACH_TRAINLINE) {
    for (EACH_DEPARTURE) {
      departures[line][dep] = 0; // + 70 * dep + 75;
    }
    depshift[line] = 0;
  }
  // calcRealDepartures();
}

void setTrainTime(int trainLine, int departureNumber, int departureTime) {
  departures[trainLine][departureNumber] = departureTime;
}

void calcRealDepartures() {
  for   (EACH_TRAINLINE) {
    // depshift[line] = 0;
    for (EACH_DEPARTURE) {
      if (departures[line][dep] != -999) {
        int timediff = (departures[line][dep] - timeSinceUpdate);
        int timediffmin = timediff / 60;
        int disptime = max(timediffmin, 0);
        if (disptime == 0)
          depshift[line]++;
        departures_real[line][dep] = disptime;
      } else {
        departures_real[line][dep] = -999;
      }
    }
  }
  // Serial.print("Y");



  for   (EACH_TRAINLINE) {
    // for (int dep  = 0; dep  < NUM_DEPARTURETIMES - depshift[line]; dep++ ) {
    for (EACH_DEPARTURE) {
      int realdeptime = departures_real[line][dep]; // + depshift[line]];
      if (realdeptime != -999) {
        SetFrameValueInt (line, dep, realdeptime);
      } else {
        SetFrameIcon (line, dep, 2);
      }
    }
    // for (int dep  = NUM_DEPARTURETIMES - depshift[line]; dep < NUM_DEPARTURETIMES; dep++ ) {
    //   SetFrameIcon (line, dep, 1);
    // }
  }
  // Serial.print("Z");
  SetAllDisplaysFrameFull(0);
  WriteAllDisplays();
}

void EnableTrains() {
  calcRealDepartures();
  trainsready = 1;
}

int TrainsReady() {
  return trainsready;
}
