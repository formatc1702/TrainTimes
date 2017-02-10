#ifndef __LEDS_H
#define __LEDS_H

void InitDisplay();
void AnimateLoading();
void SetDisplayDepartures();
void SetAllDisplaysFrameFull       (                   int FrameNumber);
void SetDisplayFrameFull           (int DisplayNumber, int FrameNumber);
void SetAllDisplaysVerticalSplit   (                   int FrameNumber1, int FrameNumber2, int Split);
void SetDisplayFrameVerticalSplit  (int DisplayNumber, int FrameNumber1, int FrameNumber2, int Split);
void SetAllDisplaysHorizontalSplit (                   int FrameNumber1, int FrameNumber2, int Split);
void SetDisplayFrameHorizontalSplit(int DisplayNumber, int FrameNumber1, int FrameNumber2, int Split);
void WriteAllDisplays();
#endif
