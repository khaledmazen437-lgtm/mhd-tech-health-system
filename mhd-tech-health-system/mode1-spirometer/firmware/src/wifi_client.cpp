#include "wifi_client.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void connectWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("Connected. IP: ");
    Serial.println(WiFi.localIP());
}

bool postReading(const String& sessionId, const SpirometryResult& result) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi not connected — cannot post reading.");
        return false;
    }

    HTTPClient http;
    http.begin(String(BACKEND_HOST) + "/device/reading");
    http.addHeader("Content-Type", "application/json");

    JsonDocument doc;
    doc["session_id"] = sessionId;
    doc["fvc"] = result.fvc;
    doc["fev1"] = result.fev1;
    doc["pef"] = result.pef;

    String payload;
    serializeJson(doc, payload);

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
        Serial.printf("POST /device/reading -> %d\n", httpResponseCode);
    } else {
        Serial.printf("POST failed: %s\n", http.errorToString(httpResponseCode).c_str());
    }

    http.end();
    return httpResponseCode == 200;
}
