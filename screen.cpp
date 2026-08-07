#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "screen.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1        // Reset pin (-1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C     // Standard I2C address for 128x64 OLEDs

static Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void screenInit(void) {
    // Initialize I2C communication using the pins specified in pinout.h[cite: 3]
    Wire.begin(OLED_SDA_PIN, OLED_SCL_PIN);

    // Initialize the OLED display with the SSD1306 switchcap VCC
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
        Serial.println(F("ERROR: SSD1306 allocation failed"));
        for (;;); // Don't proceed, loop forever if display fails
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println(F("System Initializing..."));
    display.display();
}

void screenTask(void) {
    static uint32_t lastUpdate_ms = 0;
    static const uint32_t updatePeriod_ms = 500; // Refresh every 500ms
    uint32_t currentTime_ms = millis();

    if (lastUpdate_ms + updatePeriod_ms <= currentTime_ms) {
        lastUpdate_ms = currentTime_ms;

        display.clearDisplay();
        display.setCursor(0, 0);
        
        // Example layout for system telemetry
        display.println(F("--- ROBOT 1 STATUS ---"));
        display.print(F("IP: "));
        display.println(WiFi.localIP());
        
        display.display();
    }
}