#include "statemachines.h"
#include "leds.h"
#include "config.h"

SM LedSM (FrameLoadingHead, FrameLoadingBody);

void ExecLedSM() {
  EXEC(LedSM);
};

State FrameLoadingHead() {
  AnimateLoading();
}

State FrameLoadingBody() {
  if(LedSM.Timeout(FRAME_SCROLLDELAY)) {
    LedSM.Set(FrameLoadingHead, FrameLoadingBody);
  }
}
