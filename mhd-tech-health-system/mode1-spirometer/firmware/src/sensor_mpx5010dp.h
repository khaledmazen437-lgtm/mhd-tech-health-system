#ifndef SENSOR_MPX5010DP_H
#define SENSOR_MPX5010DP_H

#include <Arduino.h>

// MPX5010DP: 0-10 kPa differential pressure sensor.
// Output: 0.2V (at 0 kPa) to 4.7V (at 10 kPa), roughly linear.
// Adjust ADC_PIN to whatever GPIO you wired the sensor's analog output to.
#define ADC_PIN 34
#define ADC_MAX_VALUE 4095.0   // ESP32 ADC is 12-bit
#define ADC_REF_VOLTAGE 3.3    // ESP32 ADC reference voltage (check your board's actual Vref)

// MPX5010DP transfer function (from datasheet): Vout = Vs * (0.09 * P + 0.04)
// Solve for P (kPa) given Vout and Vs = 5.0V supply.
// NOTE: If you're reading Vout through a voltage divider (because ESP32 ADC
// maxes at 3.3V but sensor output can reach 4.7V), account for the divider
// ratio here too. Calibrate against a known reference before trusting values.
#define SENSOR_SUPPLY_VOLTAGE 5.0
#define VOLTAGE_DIVIDER_RATIO 1.515  // e.g. if using a divider to bring 5V range into 3.3V ADC range — TUNE THIS

float readRawVoltage();
float readPressureKPa();

#endif
