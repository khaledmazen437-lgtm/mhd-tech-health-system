#ifndef WIFI_CLIENT_H
#define WIFI_CLIENT_H

#include <Arduino.h>
#include "spirometry_calc.h"

// TODO: move these to a gitignored secrets.h before committing, or use
// WiFiManager for runtime configuration instead of hardcoded credentials.
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define BACKEND_HOST "http://192.168.1.100:8000"  // your backend's LAN IP:port

void connectWiFi();
bool postReading(const String& sessionId, const SpirometryResult& result);

#endif
