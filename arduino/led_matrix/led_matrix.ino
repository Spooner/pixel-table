
#include <FastLED.h>

#define NUM_LEDS 16
#define PIN 6
#define BRIGHTNESS 64


CRGB leds[NUM_LEDS];  
int r, g, b, i;

void setup() {
  FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS);//.setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  Serial.begin(115200);
  FastLED.show();
}

void loop() {
  for (i = 0; i < NUM_LEDS; ++i) {
    while (Serial.available() < 3);

    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
    leds[i] = CRGB(r, g, b);
    Serial.print(r, HEX);
    Serial.print(g, HEX);
    Serial.print(b, HEX);
    Serial.print(" ");
  }
  FastLED.show();
  Serial.println("END");
}

