# ESP32 Spirometer Firmware

## Build & Flash (PlatformIO)

```bash
pio run -t upload
pio device monitor
```

## Wiring (MPX5010DP → ESP32)

| MPX5010DP Pin | ESP32 |
|---|---|
| Vout | GPIO34 (via voltage divider — see `sensor_mpx5010dp.h`) |
| Vs (Supply) | 5V |
| GND | GND |

**Important:** the MPX5010DP outputs 0.2V–4.7V, but the ESP32 ADC only reads 0–3.3V safely. Use a voltage divider (or level shifter) and tune `VOLTAGE_DIVIDER_RATIO` in `sensor_mpx5010dp.h` to match your actual resistor values — do not feed the raw sensor output directly into the ADC pin.

## Before real patient use

- [ ] Calibrate `FLOW_CALIBRATION_CONST` in `spirometry_calc.cpp` against a certified 3L calibration syringe
- [ ] Verify `VOLTAGE_DIVIDER_RATIO` against a multimeter reading of actual divider output
- [ ] Move WiFi credentials out of `wifi_client.h` into a gitignored `secrets.h`
- [ ] Replace the hardcoded `currentSessionId` stub with a real session-handoff mechanism from the backend

## TODO: Future sensor additions

- MAX30102 (SpO2 & Pulse) — I2C, add alongside existing ADC read loop
- DHT11/22 (Room Temp & Humidity) — single-wire digital, low priority
