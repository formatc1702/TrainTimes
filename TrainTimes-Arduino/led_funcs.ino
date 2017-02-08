//#include "LedControl.h"
#include "displaychars.h"
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Max72xxPanel.h>

#define PIN_CS   A2
#define PIN_DIN  A3
#define PIN_CLK  A4
#define PIN_LOAD A2

#define NUM_DISPLAYS NUM_TRAINLINES
#define NUM_FRAMES   NUM_DEPARTURETIMES + 1 // one blank frame

//LedControl lc = LedControl(PIN_DIN, PIN_CLK, PIN_LOAD, NUM_DISPLAYS);
Max72xxPanel matrix = Max72xxPanel(PIN_CS, NUM_DISPLAYS, 1);

#define LED_INTENSITY 3

#define RED 0
#define GREEN 1

#define FRAME_CUSTOM 32767

char FrameBuffer[NUM_DISPLAYS][NUM_FRAMES][8];

char OutputBuffer[NUM_DISPLAYS][8];
int CurrentFrame[NUM_DISPLAYS];

boolean DisplayColor[NUM_DISPLAYS] = {RED, GREEN};

// INITIALIZATION ////////////////////////////////////////////////////////////

void InitDisplay() {
  matrix.shutdown(false); // turn on
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    for (int r = 0; r < 8; r++) {
      OutputBuffer[i][r] = 0x00;
      for (int f = 0; f < NUM_FRAMES; f++) {
        FrameBuffer[i][f][r] = 0;
      }
    }
    CurrentFrame[i] = 0;

    //        lc.setIntensity(i, LED_INTENSITY);
    //    matrix.setRotation(i, 3);
    //    matrix.fillScreen(1);
    //        lc.clearDisplay(i);
    //     lc.shutdown(i,false); // disable green displays
    //    lc.shutdown(i, DisplayColor[i] == GREEN); // disable green displays
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

  //  matrix.drawPixel(8, 0, 1);
  //  matrix.write();
  //  delay(100);
  //  matrix.drawPixel(8, 7, 1);
  //  matrix.write();
  //  delay(100);
  //  matrix.drawPixel(15, 0, 1);
  //  matrix.write();
  //  delay(100);
  //  matrix.drawPixel(15, 7, 1);
  //  matrix.write();
  //  delay(100);
  matrix.setIntensity(LED_INTENSITY);
  // matrix.fillScreen(1);
  // matrix.write();
  // delay(500);
  matrix.fillScreen(0);
  matrix.write();
}

void SetDisplayFrame(int DisplayNumber, int FrameNumber) {
  for (int r = 0; r < 8; r++) {
    OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber][r];
  }
}

void SetDisplay(int DisplayNumber, char DisplayRows[]) {
  for (int r = 0; r < 8; r++) {
    OutputBuffer[DisplayNumber][r] = DisplayRows[r];
  }
}

// SET DISPLAY FRAME /////////////////////////////////////////////////////////////

void SetFrameRaw(int DisplayNumber, int FrameNumber, char Value[8]) {
  for (int r = 0; r < 8; r++) {
    FrameBuffer[DisplayNumber][FrameNumber][r] = Value[r];
  }
}

void SetFrameValueInt(int DisplayNumber, int FrameNumber, int Value) {
  char _buf[8];
  int _val;

  _val = abs(Value);
  _val = _val % 100;

  int _ones = _val % 10;
  int _tens = _val / 10;
  for (int r = 0; r < 8; r++) {
    if (_tens > 0) {
      _buf[r] = (numbers[_tens][r] << 4) | numbers[_ones][r];
    } else {
      _buf[r] = numbers[_ones][r];
    }
    FrameBuffer[DisplayNumber][FrameNumber][r] = _buf[r];
  }
}

void SetFrameIcon(int DisplayNumber, int FrameNumber, int Value) {
  for (int r = 0; r < 8; r++) {
    FrameBuffer[DisplayNumber][FrameNumber][r] = icons[Value][r];
  }
}

// FILL BUFFER ////////////////////////////////////////////////////////////////////

void SetDisplayFrameFull(int DisplayNumber, int FrameNumber) {
  CurrentFrame[DisplayNumber] = FrameNumber;
  for (int r = 0; r < 8; r++) {
    OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber][r];
  }
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
  for (int r = 0; r < 8; r++) {
    OutputBuffer[DisplayNumber][r]  =  FrameBuffer[DisplayNumber][FrameNumber1][r] << Split;
    OutputBuffer[DisplayNumber][r] |= (FrameBuffer[DisplayNumber][FrameNumber2][r] >> 8 - Split);
    // OutputBuffer[DisplayNumber][r] = FrameBuffer[DisplayNumber][FrameNumber1+Split][r];
  }
}

// OUTPUT BUFFER TO HARDWARE ///////////////////////////////////////////////

void WriteDisplay(int DisplayNumber) {
  //  lc.clearDisplay(DisplayNumber);
  for (int r = 0; r < 8; r++) {
    for (int c = 0; c < 8; c++) {
      //          lc.setColumn(DisplayNumber, r, OutputBuffer[DisplayNumber][r]);
      int realrow = r + 8 * DisplayNumber;
      //      Serial.print(DisplayNumber);
      //      Serial.print('\t');
      //      Serial.print(realrow);
      //      Serial.println();
      matrix.drawPixel(realrow, c, (OutputBuffer[DisplayNumber][r] << c & B10000000));
    }
  }
  //  Serial.println();
  matrix.write();
}

boolean blinky = false;

void WriteAllDisplays() {
  //  long before = millis();
  for (int i = 0; i < NUM_DISPLAYS; i++) {
    //    OutputBuffer[i][7] = B01000000 << blinky; //OutputBuffer[i][7] | (blinky << 7);
    WriteDisplay(i);
  }
  //  long after = millis();
  //    blinky = !blinky;
  //  Serial.print("took ");
  //  Serial.println(after - before, DEC);
}

void SleepDisplays() {
  matrix.shutdown(true); // turn off
}

// */
