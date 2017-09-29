
#include <FastLED.h>

#define WIDTH 16
#define HEIGHT 16
#define NUM_LEDS (WIDTH * HEIGHT)
#define PIN 6
#define BRIGHTNESS 64


CRGB leds[NUM_LEDS];  
int r, g, b, x, y;

void setup() {
  FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS);//.setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(115200);
  FastLED.show();
}

void loop() {
  for (y = 0; y < NUM_LEDS; y++) {
    for (x = 0; x < NUM_LEDS; x++) {
      while (Serial.available() < NUM_LEDS * 3);
      b = Serial.read();
      g = Serial.read();
      r = Serial.read();
      leds[x + y * WIDTH] = CRGB(r, g, b);
    }
    Serial.print('X');
  }
  FastLED.show();
}

