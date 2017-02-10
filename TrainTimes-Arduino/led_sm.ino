SM LedSM   (FrameLoadingHead, FrameLoadingBody );

int num = 0;
int curframe = 0;
int nextframe = 0;
int splitter = 1;
int forcevar = 0;

int iconcounter = 0;

boolean scrolling = false;

#define FRAME_SCROLLDELAY 50
#define FRAME_STOPDELAY_FIRST 8000
#define FRAME_STOPDELAY_OTHERS 500
//#define UPDATE_INTERVAL 100

void ExecLedSM() {
  EXEC(LedSM);
}

void ForceFirstFrame() {
  curframe = 0;
  forcevar = 1;
  LedSM.Set(FrameStatic);
  Serial.println("ForceFirstFrame");
}

State FrameLoadingHead() {
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    SetFrameIcon(i, 0, 7 + iconcounter);
    SetDisplayFrameFull(i, 0);
  }
  matrix.drawPixel(0, 4, 0);
  WriteAllDisplays();
}

State FrameLoadingBody() {
  if(LedSM.Timeout(FRAME_SCROLLDELAY)) {
    if (++iconcounter == 20)
      iconcounter = 0;
    LedSM.Set(FrameLoadingHead, FrameLoadingBody);  
  }
}

State FrameStatic() {
  //  Serial.println("static start.");
  Serial.println("FrameStatic");
  scrolling = false;
  forcevar = 0;
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    SetDisplayFrameFull(i, curframe);
  }
  WriteAllDisplays();
  //  Serial.println("static done.");
  LedSM.Set(FrameIdle);
}

State FrameIdle() {
  //  Serial.print(".");
  if (forcevar == 1) {
    Serial.println("Idle->Static");
    LedSM.Set(FrameStatic);
  }
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
  if (forcevar == 1) {
    Serial.println("Scrolling->Static");
    LedSM.Set(FrameStatic);
  }
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    SetDisplayFrameVerticalSplit(i, curframe, nextframe, splitter);
  }
  WriteAllDisplays();
  //  Serial.println("scrolling done.");
  LedSM.Set(FrameScrollIdle);
}

State FrameScrollIdle() {
  //  Serial.print("/");
  if (forcevar == 1) {
    Serial.println("ScrollingIdle->Static");
    LedSM.Set(FrameStatic);
  }
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
