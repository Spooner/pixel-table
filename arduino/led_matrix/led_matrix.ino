
#include <FastLED.h>

#define WIDTH 16
#define HEIGHT 16
#define NUM_LEDS (WIDTH * HEIGHT)
#define PIN 6
#define BRIGHTNESS 64


CRGB leds[NUM_LEDS];  
int r, g, b;
int x, y, xx;

void setup() {
  FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS);//.setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(115200);
  FastLED.show();
}

void loop() {
  for (y = 0; y < HEIGHT; y++) {
    for (x = 0; x < WIDTH; x++) {
      while (Serial.available() < 3);
      r = Serial.read();
      g = Serial.read();
      b = Serial.read();
      if (y % 2 == 0) {
        xx = x;
      } else {
        xx = WIDTH - x - 1;
      }
      leds[xx + y * WIDTH] = CRGB(r, g, b);
    }
    Serial.print('X');
  }
  FastLED.show();
}

