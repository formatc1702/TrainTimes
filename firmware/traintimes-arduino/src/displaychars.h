const char numbers[10][8] ={
  { // 0
    0B00000000,
    0B00001110,
    0B00001010,
    0B00001010,
    0B00001010,
    0B00001010,
    0B00001110,
    0B00000000
  },
  { // 1
    0B00000000,
    0B00000010,
    0B00000110,
    0B00000010,
    0B00000010,
    0B00000010,
    0B00000010,
    0B00000000
  },
  { // 2
    0B00000000,
    0B00001100,
    0B00000010,
    0B00000010,
    0B00000100,
    0B00001000,
    0B00001110,
    0B00000000
  },
  { // 3
    0B00000000,
    0B00001100,
    0B00000010,
    0B00001100,
    0B00000010,
    0B00000010,
    0B00001100,
    0B00000000
  },
  { // 4
    0B00000000,
    0B00000010,
    0B00000110,
    0B00001010,
    0B00001110,
    0B00000010,
    0B00000010,
    0B00000000
  },
  { // 5
    0B00000000,
    0B00001110,
    0B00001000,
    0B00001110,
    0B00000010,
    0B00000010,
    0B00001100,
    0B00000000
  },
  { // 6
    0B00000000,
    0B00000110,
    0B00001000,
    0B00001110,
    0B00001010,
    0B00001010,
    0B00001110,
    0B00000000
  },
  { // 7
    0B00000000,
    0B00001110,
    0B00000010,
    0B00000010,
    0B00000100,
    0B00000100,
    0B00000100,
    0B00000000
  },
  { // 8
    0B00000000,
    0B00001110,
    0B00001010,
    0B00001110,
    0B00001010,
    0B00001010,
    0B00001110,
    0B00000000
  },
  { // 9
    0B00000000,
    0B00001110,
    0B00001010,
    0B00001110,
    0B00000010,
    0B00000010,
    0B00001100,
    0B00000000
  }
};
// */
const char icons[7][8] ={
  { // blank
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // ..
    0B00000000,
    0B00000000,
    0B00000000,
    0B01000100,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // xx
    0B00000000,
    0B00000000,
    0B10101010,
    0B01000100,
    0B10101010,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // --
    0B00000000,
    0B00000000,
    0B00000000,
    0B11101110,
    0B00000000,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  {
    0B11111111,
    0B10000001,
    0B10000001,
    0B10011001,
    0B10011001,
    0B10000001,
    0B10000001,
    0B11111111
  },
  {
    0B10000001,
    0B01000010,
    0B00100100,
    0B00011000,
    0B00011000,
    0B00100100,
    0B01000010,
    0B10000001
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  }
};

const char loading_sine[14][8] = {
  { // 1
    0B00000000,
    0B00000000,
    0B00000000,
    0B11110000,
    0B00001111,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // 2
    0B00000000,
    0B00000000,
    0B01100000,
    0B10010000,
    0B00001001,
    0B00000110,
    0B00000000,
    0B00000000,
  },
  { // 3
    0B00000000,
    0B01100000,
    0B10010000,
    0B10010000,
    0B00001001,
    0B00001001,
    0B00000110,
    0B00000000,
  },
  { // 4
    0B01100000,
    0B10010000,
    0B10010000,
    0B10010000,
    0B00001001,
    0B00001001,
    0B00001001,
    0B00000110,
  },
  { // 3
    0B00000000,
    0B01100000,
    0B10010000,
    0B10010000,
    0B00001001,
    0B00001001,
    0B00000110,
    0B00000000,
  },
  { // 2
    0B00000000,
    0B00000000,
    0B01100000,
    0B10010000,
    0B00001001,
    0B00000110,
    0B00000000,
    0B00000000,
  },
  { // 1
    0B00000000,
    0B00000000,
    0B00000000,
    0B11110000,
    0B00001111,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // -1
    0B00000000,
    0B00000000,
    0B00000000,
    0B00001111,
    0B11110000,
    0B00000000,
    0B00000000,
    0B00000000,
  },
  { // -2
    0B00000000,
    0B00000000,
    0B00000110,
    0B00001001,
    0B10010000,
    0B01100000,
    0B00000000,
    0B00000000,
  },
  { // -3
    0B00000000,
    0B00000110,
    0B00001001,
    0B00001001,
    0B10010000,
    0B10010000,
    0B01100000,
    0B00000000,
  },
  { // -4
    0B00000110,
    0B00001001,
    0B00001001,
    0B00001001,
    0B10010000,
    0B10010000,
    0B10010000,
    0B01100000,
  },
  { // -3
    0B00000000,
    0B00000110,
    0B00001001,
    0B00001001,
    0B10010000,
    0B10010000,
    0B01100000,
    0B00000000,
  },
  { // -2
    0B00000000,
    0B00000000,
    0B00000110,
    0B00001001,
    0B10010000,
    0B01100000,
    0B00000000,
    0B00000000,
  },
  { // -1
    0B00000000,
    0B00000000,
    0B00000000,
    0B00001111,
    0B11110000,
    0B00000000,
    0B00000000,
    0B00000000,
  }
};

/*
const char loading_circle[20][8] = {
  {
    0B00000100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00100000,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00110000,
    0B01000000,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111000,
    0B01000000,
    0B10000000,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000000,
    0B10000000,
    0B10000000,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B10000000,
    0B10000000,
    0B10000000,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000000,
    0B10000000,
    0B10000000,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000000,
    0B10000000,
    0B01000000,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000000,
    0B01000000,
    0B00111000
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000000,
    0B00110000
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00100000
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00000100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B00000010,
    0B00001100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B00000001,
    0B00000010,
    0B00011100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B10000001,
    0B00000001,
    0B00000001,
    0B00000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B10000001,
    0B00000001,
    0B00000001,
    0B00000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B01000010,
    0B00000001,
    0B00000001,
    0B00000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00111100,
    0B00000010,
    0B00000001,
    0B00000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00011100,
    0B00000010,
    0B00000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  },
  {
    0B00001100,
    0B00000010,
    0B10000001,
    0B10000001,
    0B10000001,
    0B10000001,
    0B01000010,
    0B00111100
  }
}; // */