#ifndef SPIROMETRY_CALC_H
#define SPIROMETRY_CALC_H

// TODO: replace placeholder tube/orifice constants with values calibrated
// against a certified 3L calibration syringe before using for real readings.
// Pressure-to-flow conversion depends on your specific tube geometry.

struct SpirometryResult {
    float fvc;   // Forced Vital Capacity (mL)
    float fev1;  // Forced Expiratory Volume in 1 second (mL)
    float pef;   // Peak Expiratory Flow (mL/s)
};

// Call this repeatedly during a ~6-second forced exhalation, feeding it
// pressure readings (kPa) at each sample interval, then call finalize().
class SpirometryCalculator {
public:
    void reset();
    void addSample(float pressureKPa, unsigned long timestampMs);
    SpirometryResult finalize();

private:
    float volumeAccumulatedML = 0;
    float peakFlowMLperS = 0;
    float volumeAt1SecML = 0;
    unsigned long startTimeMs = 0;
    bool started = false;

    float pressureToFlow(float pressureKPa);  // mL/s, needs calibration constant
};

#endif
