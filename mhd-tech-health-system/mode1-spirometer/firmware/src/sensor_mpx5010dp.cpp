#include "sensor_mpx5010dp.h"

float readRawVoltage() {
    int raw = analogRead(ADC_PIN);
    float v_at_pin = (raw / ADC_MAX_VALUE) * ADC_REF_VOLTAGE;
    return v_at_pin * VOLTAGE_DIVIDER_RATIO;  // scale back up to sensor's actual output voltage
}

float readPressureKPa() {
    float vout = readRawVoltage();
    // Vout = Vs * (0.09 * P + 0.04)  =>  P = (Vout / Vs - 0.04) / 0.09
    float pressure_kpa = (vout / SENSOR_SUPPLY_VOLTAGE - 0.04) / 0.09;
    return pressure_kpa;
}
