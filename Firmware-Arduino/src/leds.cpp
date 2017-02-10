#include <SPI.h>
#include "Adafruit_GFX.h"
#include "Max72xxPanel.h"

#include "config.h"
#include "displaychars.h"

#define PIN_CS   A2
#define PIN_DIN  A3
#define PIN_CLK  A4
#define PIN_LOAD A2

#define LED_INTENSITY 7

#define NUM_DISPLAYS NUM_TRAINLINES
#define NUM_FRAMES   NUM_DEPARTURETIMES + 1 // one blank frame

#define FRAME_CUSTOM 32767

// for loop macros
#define EACH_DISPLAY int i = 0; i < NUM_DISPLAYS; i++
#define EACH_FRAME   int f = 0; f < NUM_FRAMES;   f++
#define EACH_ROW     int r = 0; r < 8;            r++
#define EACH_COL     int c = 0; c < 8;            c++


Max72xxPanel matrix = Max72xxPanel(PIN_CS, NUM_DISPLAYS, 1);

char FrameBuffer  [NUM_DISPLAYS][NUM_FRAMES][8];
char OutputBuffer [NUM_DISPLAYS]            [8];
int CurrentFrame  [NUM_DISPLAYS];

// Setup
void InitDisplay() {
  matrix.shutdown(false); // turn on
   for (EACH_DISPLAY) {
    for (EACH_ROW) {
      OutputBuffer[i][r] = 0x00;
      for (EACH_FRAME)
        FrameBuffer[i][f][r] = 0;
    }
    CurrentFrame[i] = 0;
  }
  matrix.setPosition(0, 0, 0);
  matrix.setPosition(1, 0, 1);

  matrix.setRotation(0, 0);
  matrix.setRotation(1, 2);
  matrix.setRotation(2, 0);
  matrix.setRotation(3, 2);
  matrix.setRotation(4, 0);
  matrix.setRotation(5, 2);
  matrix.setRotation(6, 0);
  matrix.setRotation(7, 2);
  matrix.setIntensity(LED_INTENSITY);
  // matrix.fillScreen(1);
  // matrix.write();
  // delay(500);
  matrix.fillScreen(0);
  matrix.write();
}

// Actual output to IC
void WriteDisplay(int DisplayNumber) {
  for (EACH_ROW) {
    for (EACH_COL) {
      int realrow = r + 8 * DisplayNumber;
      matrix.drawPixel(realrow, c, (OutputBuffer[DisplayNumber][r] << c & B10000000));
    }
  }
  matrix.write();
}

void WriteAllDisplays() {
  for (EACH_DISPLAY)
    WriteDisplay(i);
}

// Frames and stuff
void SetFrameIcon(int DisplayNumber, int FrameNumber, int Value) {
  for (EACH_ROW)
    FrameBuffer[DisplayNumber][FrameNumber][r] = icons[Value][r];
}

void SetFrameLoading(int DisplayNumber, int FrameNumber, int Value) {
  for (EACH_ROW)
    FrameBuffer[DisplayNumber][FrameNumber][r] = loading_sine[Value][r];
}

void SetDisplayFrameFull(int DisplayNumber, int FrameNumber) {
  CurrentFrame[DisplayNumber] = FrameNumber;
  for (EACH_ROW)
    OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber][r];
}

void SetDisplayFrameVerticalSplit(int DisplayNumber, int FrameNumber1, int FrameNumber2, int Split) {
  CurrentFrame[DisplayNumber] = FRAME_CUSTOM;
  for (int r = 0; r < (8 - Split); r++) {
    OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber1][r + Split];
    // OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber1+Split][r];
  }
  for (int r = (8 - Split); r < 8; r++) {
    OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber2][r - (8 - Split)];
    // OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber2+(8-Split)][r];
  }
}

void SetDisplayFrameHorizontalSplit(int DisplayNumber, int FrameNumber1, int FrameNumber2, int Split) {
  CurrentFrame[DisplayNumber] = FRAME_CUSTOM;
  for (EACH_ROW) {
    OutputBuffer[DisplayNumber][r]  =  FrameBuffer[DisplayNumber][FrameNumber1][r] << Split;
    OutputBuffer[DisplayNumber][r] |= (FrameBuffer[DisplayNumber][FrameNumber2][r] >> (8 - Split));
  }
}

void SetFrameValueInt(int DisplayNumber, int FrameNumber, int Value) {
  char _buf[8];
  int _val;
  _val = abs(Value);
  _val = _val % 100;
  int _ones = _val % 10;
  int _tens = _val / 10;

  for (EACH_ROW) {
    if (_tens > 0)
      _buf[r] = (numbers[_tens][r] << 4) | numbers[_ones][r];
    else
      _buf[r] = numbers[_ones][r];
    FrameBuffer[DisplayNumber][FrameNumber][r] = _buf[r];
  }
}

void AnimateLoading() {
  static int _loading_frame = 0;
  for (EACH_DISPLAY) {
    SetFrameLoading    (i, 0, _loading_frame);
    SetDisplayFrameFull(i, 0);
  }
  WriteAllDisplays();
  if (++_loading_frame == 14)
    _loading_frame = 0;
}
