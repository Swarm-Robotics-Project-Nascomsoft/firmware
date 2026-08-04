#include <stdint.h>

#ifndef PINOUT_H
#define PINOUT_H


// --- Unchanged from original repo ---
const uint8_t ELECTROMAGNET_PIN = 2;   // kept: no firmware change needed, still a plain
                                        // digitalWrite() target - MOSFET driver stage is a
                                        // hardware-side addition, not a pin change
const uint8_t HEARTBEAT_PIN = 14;      // kept: heartbeat LED logic unchanged - TODO confirm
                                        // this GPIO is still free/valid on the new board

// --- Removed from original repo ---
// const uint8_t NEOPIXEL_PIN  -> REMOVED: NeoPixel dropped entirely from this build
// const uint8_t SERVO1_PIN    -> REMOVED: no continuous-rotation servos anymore
// const uint8_t SERVO2_PIN    -> REMOVED: no continuous-rotation servos anymore
// const uint8_t BUTTON_PIN    -> REMOVED: robot ID is HTTP-only now, no physical button poll.
//                                 (Also worth remembering: old value was GPIO0, a strapping
//                                 pin - avoid reusing GPIO0 for a button if this ever comes back.)

// --- NEW: L298N drivetrain pins (Module 1) ---
// TODO: confirm all 6 against tomorrow's breadboard wiring. Placeholder values below are
// spaced out and arbitrary - they do NOT reflect real ESP32 DevKit pin suitability
// (e.g. avoid input-only pins for outputs, avoid strapping pins, avoid ADC2 pins if WiFi is
// active). Pick real values tomorrow with the datasheet in hand.
const uint8_t MOTOR1_IN1_PIN = 32;   // TODO CONFIRM
const uint8_t MOTOR1_IN2_PIN = 33;   // TODO CONFIRM
const uint8_t MOTOR1_ENA_PIN = 25;   // TODO CONFIRM - must support LEDC PWM output
const uint8_t MOTOR2_IN3_PIN = 26;   // TODO CONFIRM
const uint8_t MOTOR2_IN4_PIN = 27;   // TODO CONFIRM
const uint8_t MOTOR2_ENB_PIN = 13;   // TODO CONFIRM - must support LEDC PWM output

// --- NEW: Battery voltage sense (Module 3) ---
const uint8_t BATT_SENSE_PIN = 34;   // TODO CONFIRM - GPIO34 is ADC1-only, input-only, good
                                      // candidate for analog sense, but confirm against final
                                      // board/wiring tomorrow

// --- NEW: OLED I2C (Module 4) ---
// TODO: ESP32 default I2C pins are often SDA=21/SCL=22, but confirm against the specific
// DevKit/NodeMCU board in hand tomorrow - not all ESP32 boards break these out the same way.
const uint8_t OLED_SDA_PIN = 21;   // TODO CONFIRM
const uint8_t OLED_SCL_PIN = 22;   // TODO CONFIRM

#endif /* PINOUT_H */
