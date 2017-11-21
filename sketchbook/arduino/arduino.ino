# https://github.com/kosme/arduinoFFT/blob/master/Examples/FFT_03/FFT_03.ino

#include <arduinoFTT.h>

const uint16_t num_samples = 64; // This value MUST ALWAYS be a power of 2
const double samplingFrequency = 1000.0;  // 1000 samples per second.
const int delayTime = 1000 / samplingFrequency;

uint8_t exponent;

// These are the input and output vectors
// Input vectors receive computed results from FFT
double vReal[num_samples];
double vImag[num_samples];

#define MICROPHONE A0

void setup()
{
    Serial.begin(115200);
    exponent = FFT.Exponent(num_samples);
}

void loop()
{
    Serial.read();

    for (uint16_t i = 0; i < num_samples; i++)
    {
        vReal[i] = double(analogRead(MICROPHONE);
        delay(delayTime);
    }
    memset(vImag[i], 0, num_samples);

    FFT.Windowing(vReal, num_samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);	// Weigh data
    FFT.Compute(vReal, vImag, num_samples, FFT_FORWARD); // Compute FFT
    FFT.ComplexToMagnitude(vReal, vImag, num_samples); // Compute magnitudes

    for (uint16_t i = 0; i < (num_samples >> 1); i++)
    {
        Serial.print(vReal[i]);
        Serial.print(',');
    }
    Serial.printLn();
}
