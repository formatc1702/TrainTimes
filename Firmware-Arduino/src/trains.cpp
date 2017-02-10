#include "trains.h"
#include <Arduino.h> // max()

#include "config.h"
#define RECALC_TIMES_SECONDS 3

#define EACH_TRAINLINE int line = 0; line < NUM_TRAINLINES;     line++
#define EACH_DEPARTURE int dep  = 0; dep  < NUM_DEPARTURETIMES; dep++
int departures      [NUM_TRAINLINES][NUM_DEPARTURETIMES];
int departures_real [NUM_TRAINLINES][NUM_DEPARTURETIMES];
int depshift        [NUM_TRAINLINES];

int timeSinceUpdate = 0;


void InitTrains() {
  for   (EACH_TRAINLINE) {
    for (EACH_DEPARTURE) {
      departures[line][dep] = 0; // + 70 * dep + 75;
    }
    depshift[line] = 0;
  }
  calcRealDepartures();
}

void calcRealDepartures() {
  for   (EACH_TRAINLINE) {
    depshift[line] = 0;
    for (EACH_DEPARTURE) {
      if (departures[line][dep] != -999) {
        int timediff = (departures[line][dep] - timeSinceUpdate);
        int timediffmin = timediff / 60;
        int disptime = max(timediffmin, 0);
        if (disptime == 0)
          depshift[line]++;
        departures_real[line][dep] = disptime;

//        Serial.print(timediff);
//        Serial.print('\t');
      } else {
        departures_real[line][dep] = -999;
      }
    }
//    Serial.println();
  }
//  Serial.println();
}

int TrainsReady() {
  return 0;
}
