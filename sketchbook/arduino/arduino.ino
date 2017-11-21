// https://github.com/kosme/arduinoFFT/blob/master/Examples/FFT_03/FFT_03.ino

#include <arduinoFFT.h>
arduinoFFT FFT = arduinoFFT(); // Create FFT object

const uint16_t num_samples = 256; // This value MUST ALWAYS be a power of 2
const double samplingFrequency = 20000.0;  // samples per second.
const int delayTime = 1000000 / samplingFrequency;

// These are the input/output vectors
// Input vectors receive computed results from FFT
double vReal[num_samples];
double vImag[num_samples];

#define MICROPHONE A0

void setup()
{
    Serial.begin(115200);
    Serial.write("R");
}

void loop()
{
    Serial.read();

    for (uint16_t i = 0; i < num_samples; i++)
    {
        vReal[i] = double(analogRead(MICROPHONE));
        delayMicroseconds(delayTime);
    }
    memset(vImag, 0, num_samples);

    FFT.Windowing(vReal, num_samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);	// Weigh data
    FFT.Compute(vReal, vImag, num_samples, FFT_FORWARD); // Compute FFT
    FFT.ComplexToMagnitude(vReal, vImag, num_samples); // Compute magnitudes

    for (uint16_t i = 0; i < (num_samples >> 1); i++)
    {
        Serial.print(vReal[i]);
        Serial.print(';');
    }
    Serial.println();
}
