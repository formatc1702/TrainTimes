SM TimerSM (TimerWaiting);

int time[7]; // Y,M,D,h,m,s,timezone
int departures[NUM_TRAINLINES][NUM_DEPARTURETIMES];
int departures_real[NUM_TRAINLINES][NUM_DEPARTURETIMES];
int weatherconditions[3];

#define YEAR 0
#define MONTH 1
#define DAY 2
#define HOUR 3
#define MINUTE 4
#define SECOND 5
#define TIMEZONE 6

#define WEATHERTYPE 0
#define TEMPERATURE 1
#define RAINTIME 2

#define RECALC_TIMES_SECONDS 3

int timeSinceUpdate = 0;

int depshift[NUM_TRAINLINES];

void ExecTimerSM() {
    EXEC(TimerSM);
}

void InitTrains() {
  for   (int line = 0; line < NUM_TRAINLINES;     line++) {
    for (int dep  = 0; dep  < NUM_DEPARTURETIMES; dep++ ) {
      departures[line][dep] = 0; // + 70 * dep + 75;
    }
    depshift[line] = 0;
  }
  calcRealDepartures();
}

void setTime(int component, int value) {
  time[component] = value;
}

void setTrainTime(int trainLine, int departureNumber, int departureTime) {
  departures[trainLine][departureNumber] = departureTime;
}

int getTrainTime(int trainLine, int departureNumber) {
  return departures[trainLine][departureNumber];
}

void setWeather(int component, int value) {
  weatherconditions[component] = value;
}

void incUpdateTime() {
  timeSinceUpdate += RECALC_TIMES_SECONDS;
}

void resetUpdateTime() {
  timeSinceUpdate = 0;
}



State TimerWaiting() {
  if (TimerSM.Timeout(RECALC_TIMES_SECONDS * 1000)) {
    TimerSM.Set(TimerTriggered);
  }
}

State TimerTriggered() {
  incUpdateTime();
  TimerSM.Set(TimerUpdating);
}

State TimerUpdating() {
  if (scrolling == false) {
    calcRealDepartures();
    Serial.println(depshift[0]);
    for   (int line = 0; line < NUM_TRAINLINES;     line++) {
      for (int dep  = 0; dep  < NUM_DEPARTURETIMES - depshift[line]; dep++ ) {
        int realdeptime = departures_real[line][dep + depshift[line]];
        if (realdeptime != -999) {
          SetFrameValueInt (line, dep, realdeptime);
        } else {
          SetFrameIcon (line, dep, 2);
        }
      }
      for (int dep  = NUM_DEPARTURETIMES - depshift[line]; dep < NUM_DEPARTURETIMES; dep++ ) {
        SetFrameIcon (line, dep, 1);
      }
    }
    //      Serial.println();
    TimerSM.Set(TimerWaiting);
  }
  //    Serial.println();
}


void calcRealDepartures() {
  for   (int line = 0; line < NUM_TRAINLINES;     line++) {
    depshift[line] = 0;
    for (int dep  = 0; dep  < NUM_DEPARTURETIMES; dep++ ) {
      if (departures[line][dep] != -999) {
        int timediff = (departures[line][dep] - timeSinceUpdate);
        int timediffmin = timediff / 60;
        int disptime = max(timediffmin, 0);
        if (disptime == 0)
          depshift[line]++;
        departures_real[line][dep] = disptime;

        Serial.print(timediff);
        Serial.print('\t');
      } else {
        departures_real[line][dep] = -999;
      }
    }
    Serial.println();
  }
  Serial.println();
}

// */
