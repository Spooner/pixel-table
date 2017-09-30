
#include <FastLED.h>

#define WIDTH 16
#define HEIGHT 16
#define NUM_LEDS (WIDTH * HEIGHT)
#define PIN 6
#define BRIGHTNESS 32

CRGB leds[NUM_LEDS];  
int r, g, b;
int x, y, yy;

void setup() {
  FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(115200);

  for (x = 0; x < 3; x++) {
    leds[0] = CRGB(0.5, 0.5, 0.5);
    FastLED.show();
    delay(200);
    leds[0] = CRGB(0, 0, 0);
    FastLED.show();
  }
}

void loop() {
  for (x = 0; x < WIDTH; x++) {
    for (y = 0; y < HEIGHT; y++) {
      while (Serial.available() < 3);
      g = Serial.read();
      r = Serial.read();
      b = Serial.read();
      if (x % 2 == 0) {
        yy = y;
      } else {
        yy = HEIGHT - y - 1;
      }
      leds[yy + x * HEIGHT] = CRGB(r, g, b);
    }
    Serial.print('X');
  }
  FastLED.show();
}

