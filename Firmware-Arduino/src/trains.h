#ifndef __TRAINS_H
#define __TRAINS_H

#define EACH_TRAINLINE int line = 0; line < NUM_TRAINLINES;     line++
#define EACH_DEPARTURE int dep  = 0; dep  < NUM_DEPARTURETIMES; dep ++

void InitTrains();
void setTrainTime(int trainLine, int departureNumber, int departureTime);
void calcRealDepartures();
void EnableTrains();
int TrainsReady();

#endif
