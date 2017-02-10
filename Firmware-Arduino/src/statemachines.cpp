#include "statemachines.h"
#include "leds.h"
#include "trains.h"
#include "config.h"

SM LedSM   (FrameLoadingHead, FrameLoadingBody);

boolean scrolling = false;

int curframe = 0;
int nextframe = 0;
int splitter = 1;
// int forcevar = 0;

void ExecStatemachines() {
  EXEC(LedSM);
};

// Loading screen animation ///////////////////////////////////
void SetDisplayLoading() {
  LedSM.Set(FrameLoadingHead, FrameLoadingBody);
}

State FrameLoadingHead() {
  AnimateLoading();
}
State FrameLoadingBody() {
  if(TrainsReady() == 1)
    LedSM.Set(FrameStaticHead, FrameStaticBody);
  if(LedSM.Timeout(FRAME_SCROLLDELAY))
    LedSM.Set(FrameLoadingHead, FrameLoadingBody);
}

// Number scrolling animation /////////////////////////////////
State FrameStaticHead() {
  scrolling = false;
  // forcevar = 0;
  SetAllDisplaysFrameFull(curframe);
  WriteAllDisplays();
}
State FrameStaticBody() {
  // if (forcevar == 1) {
  //   Serial.println("Idle->Static");
  //   LedSM.Set(FrameStaticHead, FrameStaticBody);
  // }
  if ((curframe == 0 && LedSM.Timeout(FRAME_STOPDELAY_FIRST )) || // begin scrolling from first dep.time
      (curframe  > 0 && LedSM.Timeout(FRAME_STOPDELAY_OTHERS)) || // continue scrolling through dep.times
       curframe == NUM_DEPARTURETIMES) {                          // loop around to first dep.time again
    splitter = 1;
    nextframe = curframe + 1;
    if (nextframe >= NUM_DEPARTURETIMES + 1) // +1 because of extra empty frame between last and first dep.time
      nextframe = 0;
    scrolling = true;
    LedSM.Set(FrameScrollingHead, FrameScrollingBody);
  }
}

State FrameScrollingHead() {
  SetAllDisplaysVerticalSplit(curframe, nextframe, splitter);
  WriteAllDisplays();
}
State FrameScrollingBody() {
  if (LedSM.Timeout(FRAME_SCROLLDELAY)) {
    splitter++;
    if (splitter == 8) { // finished scrolling
      curframe = nextframe;
      LedSM.Set(FrameStaticHead, FrameStaticBody);
    }
    else                 // keep scrolling
      LedSM.Set(FrameScrollingHead, FrameScrollingBody);
  }
}
