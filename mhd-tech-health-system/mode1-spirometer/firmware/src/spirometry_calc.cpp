#include "spirometry_calc.h"
#include <math.h>

// Placeholder calibration constant relating pressure drop across the
// orifice/tube to volumetric flow rate. MUST be calibrated empirically
// (e.g. with a certified calibration syringe) before clinical use.
#define FLOW_CALIBRATION_CONST 1000.0

void SpirometryCalculator::reset() {
    volumeAccumulatedML = 0;
    peakFlowMLperS = 0;
    volumeAt1SecML = 0;
    started = false;
}

float SpirometryCalculator::pressureToFlow(float pressureKPa) {
    // Simplified square-root relationship typical of differential-pressure
    // pneumotachographs: flow ~ sqrt(pressure). Sign preserved for direction.
    float sign = (pressureKPa < 0) ? -1.0 : 1.0;
    return sign * sqrt(fabs(pressureKPa)) * FLOW_CALIBRATION_CONST;
}

void SpirometryCalculator::addSample(float pressureKPa, unsigned long timestampMs) {
    if (!started) {
        startTimeMs = timestampMs;
        started = true;
        return;  // no delta to integrate yet on the first sample
    }

    float flowMLperS = pressureToFlow(pressureKPa);
    if (flowMLperS > peakFlowMLperS) {
        peakFlowMLperS = flowMLperS;
    }

    // NOTE: this assumes addSample() is called at a roughly fixed interval.
    // For production, pass dt explicitly instead of assuming a fixed rate.
    static const float ASSUMED_DT_S = 0.01;  // e.g. 100Hz sampling — TUNE THIS
    volumeAccumulatedML += flowMLperS * ASSUMED_DT_S;

    unsigned long elapsedMs = timestampMs - startTimeMs;
    if (elapsedMs <= 1000) {
        volumeAt1SecML = volumeAccumulatedML;
    }
}

SpirometryResult SpirometryCalculator::finalize() {
    SpirometryResult result;
    result.fvc = volumeAccumulatedML;
    result.fev1 = volumeAt1SecML;
    result.pef = peakFlowMLperS;
    return result;
}
