#include <WiFi.h>
#include <WebServer.h>
#include "server.h"
#include "screen.h"
#include "drivetrain.h"


static const char* ssid = "CMU-DEVICE";
static const char* password = "";

static WebServer server(80);

void handlerFunction() {
    const String dtype = server.arg("dtype");

    if (dtype == "speed") {
        drivetrainSetSpeed((uint8_t) server.arg("servo1").toInt(), (uint8_t) server.arg("servo2").toInt());

    } else if (dtype == "pallet") {
        int pallet = server.arg("power").toInt();
        if (pallet == HIGH) {
            digitalWrite(ELECTROMAGNET_PIN, HIGH);
        } else {
            digitalWrite(ELECTROMAGNET_PIN, LOW);
        }
    } else if (dtype == "robotNumber") {
        // TODO(Module 4): once robotid.cpp/robotid.h exist, replace this comment with:
        //   robotIdSetNumber((uint8_t) server.arg("robotNumber").toInt());
        // Left as a no-op for now so this file compiles independently of Module 4's status.
    }

    server.send(200, "text/html", "");
}

void serverInit(void) {
    pinMode(ELECTROMAGNET_PIN, OUTPUT);
    digitalWrite(ELECTROMAGNET_PIN, LOW);

    WiFi.begin(ssid, password);
    while(WiFi.status() != WL_CONNECTED) {
        screenAnimateParrot();
        delay(75);
    }
    char wifiInfo[screenDataLen];
    sprintf(wifiInfo, "WiFi: %s", ssid);
    screenDisplayData(SCREEN_DATA_WIFI_CONNECTION, wifiInfo);
    char ipInfo[screenDataLen];
    sprintf(ipInfo, "IP: %s", WiFi.localIP().toString().c_str());
    screenDisplayData(SCREEN_DATA_WIFI_IP, ipInfo);
    server.on("/", handlerFunction);
    Serial.println(WiFi.localIP());
    server.begin();
}

void serverTask(void) {
    server.handleClient();
}