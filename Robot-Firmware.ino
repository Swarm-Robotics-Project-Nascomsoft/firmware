#include "pinout.h"
#include "drivetrain.h"
#include "server.h"

// Heartbeat Task
void heartbeatTask(void) {
    static uint32_t lastBlink_ms = 0;
    static const uint32_t blinkPeriod_ms = 250;
    uint32_t currentTime_ms = millis();
    if (lastBlink_ms + blinkPeriod_ms <= currentTime_ms) {
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        lastBlink_ms = currentTime_ms;
    }
}

// Voltage Sense Task
void voltageSenseTask(void) {
    static uint32_t lastSample_ms = 0;
    static const uint32_t samplePeriod_ms = 1000;
    uint32_t currentTime_ms = millis();
    if (lastSample_ms + samplePeriod_ms <= currentTime_ms) {
        // CHANGED: 12-bit ADC reading from 0 to 3.3V (ESP32) - was 10-bit/0-1V on ESP8266.
        const uint32_t maxADCValue = (1 << 12);   // CHANGED: (1<<10) -> (1<<12), ESP32 ADC is 12-bit
        const uint32_t adcVref_mV = 3300;

        const uint32_t R_TOP_kOhm = 100;
        const uint32_t R_BOTTOM_kOhm = 33;

        uint32_t adcValue = analogRead(BATT_SENSE_PIN);
        uint32_t battVoltage_mV = adcValue * adcVref_mV / maxADCValue * (R_TOP_kOhm + R_BOTTOM_kOhm) / R_BOTTOM_kOhm;

        lastSample_ms = currentTime_ms;
    }
}

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);

    analogSetPinAttenuation(BATT_SENSE_PIN, ADC_11db);


    drivetrainInit();
    serverInit();
}

void loop() {
    serverTask();
    heartbeatTask();
    voltageSenseTask();
    drivetrainTask();
}