SM LedSM   (FrameStatic );

int num = 0;
int curframe = 0;
int nextframe = 0;
int splitter = 1;

boolean scrolling = false;

#define FRAME_SCROLLDELAY 50
#define FRAME_STOPDELAY_FIRST 8000
#define FRAME_STOPDELAY_OTHERS 500
//#define UPDATE_INTERVAL 100

void ExecLedSM() {
  EXEC(LedSM);
}

State FrameStatic() {
  //  Serial.println("static start.");
  scrolling = false;
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    SetDisplayFrameFull(i, curframe);
  }
  WriteAllDisplays();
  //  Serial.println("static done.");
  LedSM.Set(FrameIdle);
}

State FrameIdle() {
  //  Serial.print(".");
  if ((
        curframe == 0 && LedSM.Timeout(FRAME_STOPDELAY_FIRST)) ||
      (curframe > 0 && LedSM.Timeout(FRAME_STOPDELAY_OTHERS)) ||
      curframe == NUM_DEPARTURETIMES) {
    splitter = 1;
    nextframe = curframe + 1;
    if (nextframe >= NUM_DEPARTURETIMES + 1)
      nextframe = 0;
    scrolling = true;
    //    Serial.println("idle goto scroll");

    LedSM.Set(FrameScrolling);
  }
}

State FrameScrolling() {
  //  Serial.println("scrolling start");
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    SetDisplayFrameVerticalSplit(i, curframe, nextframe, splitter);
  }
  WriteAllDisplays();
  //  Serial.println("scrolling done.");
  LedSM.Set(FrameScrollIdle);
}

State FrameScrollIdle() {
  //  Serial.print("/");
  if (LedSM.Timeout(FRAME_SCROLLDELAY)) {
    splitter++;
    if (splitter == 8) {
      curframe = nextframe;
      LedSM.Set(FrameStatic);
    }
    else
      LedSM.Set(FrameScrolling);
  }
}
// */
