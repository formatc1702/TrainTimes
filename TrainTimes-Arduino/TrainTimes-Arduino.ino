#include "SM.h"

#define NUM_TRAINLINES 8
#define NUM_DEPARTURETIMES 5


void setup()
{
  Serial.begin(9600);
  InitDisplay();
  InitSwitch();
  InitTrains();
  WiFiInit();
  

  Serial.println();
  Serial.println("Reset.");
  
//  SetFrameValueInt(0, 0, 0);
//  SetFrameValueInt(0, 1, 1);
//  SetFrameIcon(0, 2, 1);
}

void loop()
{
  ExecLedSM();
  ExecSwitchSM();
  ExecWifiSM();
  ExecTimerSM();
//  Serial.print(":-)");
}

