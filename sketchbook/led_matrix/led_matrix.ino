#include <Wire.h>
#include <FastLED.h>

#define WIDTH 16
#define HEIGHT 16
#define NUM_LEDS (WIDTH * HEIGHT)
#define PIN 6
#define BRIGHTNESS 8
#define BUS_ADDRESS 8

CRGB leds[NUM_LEDS];
int x, y;

void setup() {
    FastLED.addLeds<WS2812B, PIN>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS);
    FastLED.setMaxPowerInMilliWatts(7500); // 5W (5V/1.5A) for testing.
    FastLED.showColor(CRGB::Black);
    FastLED.show();

    Serial.begin(9600);

    Wire.begin(BUS_ADDRESS);
    Wire.onReceive(receiveEvent);
}

void loop() {
    delay(100);
}

void receiveEvent(int howMany) {
    while (Wire.available() >= 3) {
        x += 1;

        if (x == WIDTH) {
            x = 0;
            y += 1;

            if (y == HEIGHT) {
                y = 0;
                x = 0;
            }
        }

        int r = Serial.read();
        int g = Serial.read();
        int b = Serial.read();

        // Render alternate columns in zig-zag.
        int yy;
        if (x % 2 == 0) {
            yy = HEIGHT - y - 1;
        } else {
            yy = y;
        }

        leds[yy + x * HEIGHT] = CRGB(g, r, b);  // Seems to be running as GRB, not RGB...?

        if (x == WIDTH - 1 && y == HEIGHT - 1) {
            FastLED.show();
            Serial.write("#");
        }
    }
}
