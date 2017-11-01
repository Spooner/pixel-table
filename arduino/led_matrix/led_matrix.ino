
#include <FastLED.h>

#define WIDTH 16
#define HEIGHT 16
#define NUM_LEDS (WIDTH * HEIGHT)
#define PIN 6
#define UART_RATE 460800
#define BRIGHTNESS 8

CRGB leds[NUM_LEDS];
int r, g, b;
int x, y, yy;

void setup() {
  FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(UART_RATE);
  FastLED.show();
}

void loop() {
  Serial.write("R");

  for (x = 0; x < WIDTH; x++) {
    for (y = 0; y < HEIGHT; y++) {
      while (Serial.available() < 3);
      r = Serial.read();
      g = Serial.read();
      b = Serial.read();

      // Render alternate columns in zig-zag.
      if (x % 2 == 0) {
        yy = HEIGHT - y - 1;
      } else {
        yy = y;
      }

      leds[yy + x * HEIGHT] = CRGB(g, r, b);  // Seems to be running as GRB, not RGB...?
    }
  }
  FastLED.show();
}

