#include <Arduino.h>
#include "sensor_mpx5010dp.h"
#include "spirometry_calc.h"
#include "wifi_client.h"

// TODO: replace with a real mechanism for receiving the session_id from the
// backend/React (e.g. serial command, BLE, or a small on-device display +
// button, or polling a /session/pending endpoint). Hardcoded here as a stub.
String currentSessionId = "";

SpirometryCalculator calculator;

#define BUTTON_PIN 4          // wire a push-button to start the test
#define TEST_DURATION_MS 6000 // standard forced exhalation window
#define SAMPLE_INTERVAL_MS 10 // ~100Hz sampling

void runSpirometryTest() {
    calculator.reset();
    unsigned long testStart = millis();

    Serial.println("Test started — exhale forcefully now.");

    while (millis() - testStart < TEST_DURATION_MS) {
        float pressure = readPressureKPa();
        calculator.addSample(pressure, millis());
        delay(SAMPLE_INTERVAL_MS);
    }

    SpirometryResult result = calculator.finalize();

    Serial.printf(
        "Test complete. FVC=%.1f mL, FEV1=%.1f mL, PEF=%.1f mL/s\n",
        result.fvc, result.fev1, result.pef
    );

    if (currentSessionId.length() > 0) {
        postReading(currentSessionId, result);
    } else {
        Serial.println("No session_id set — reading not sent to backend.");
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(ADC_PIN, INPUT);

    connectWiFi();

    Serial.println("Ready. Press the button to start a spirometry test.");
}

void loop() {
    if (digitalRead(BUTTON_PIN) == LOW) {
        runSpirometryTest();
        delay(1000); // debounce / cooldown before allowing another test
    }
}
