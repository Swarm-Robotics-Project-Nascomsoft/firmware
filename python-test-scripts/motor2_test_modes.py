import time
import urllib.request
import urllib.parse

# Replace with your ESP32 robot's actual local IP address
ROBOT_IP = "172.20.10.2"
URL = f"http://{ROBOT_IP}/"

def send_motor2(servo2_val):
    """Sends a command keeping Motor 1 neutral (90) and testing Motor 2."""
    payload = urllib.parse.urlencode({"dtype": "speed", "servo1": 90, "servo2": servo2_val}).encode("utf-8")
    try:
        req = urllib.request.Request(URL, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=3) as response:
            print(f"[SUCCESS] Motor 2 set to {servo2_val} -> Status: {response.status}")
    except Exception as e:
        print(f"[ERROR] Failed to send servo2={servo2_val}: {e}")

if __name__ == "__main__":
    print(f"Starting Direct Start vs. Momentum Test on {ROBOT_IP}...\n")

    try:
        # --- TEST A: Direct Low-Speed Start ---
        print("--- TEST A: Direct Low-Speed Start ---")
        print("1. Ensuring Motor 2 is stopped (90)")
        send_motor2(90)
        time.sleep(2)

        print("2. Jumping DIRECTLY from stop to low speed (servo2 = 110)")
        print("   -> Watch closely: Does the motor actually start turning on its own?")
        send_motor2(110)
        time.sleep(4)

        print("3. Stopping motor")
        send_motor2(90)
        time.sleep(2)

        # --- TEST B: Momentum Continuation ---
        print("\n--- TEST B: Momentum Continuation ---")
        print("1. Kicking to Full Speed (servo2 = 180)")
        send_motor2(180)
        time.sleep(2)

        print("2. Dropping down to low speed while moving (servo2 = 110)")
        print("   -> Watch closely: Does it successfully keep spinning at the lower speed?")
        send_motor2(110)
        time.sleep(4)

        # 3. Stop
        print("3. Final Stop (90)")
        send_motor2(90)

        print("\nTest sequence complete. How did each test behave?")

    except KeyboardInterrupt:
        print("\n\nTest stopped. Sending safety stop...")
        send_motor2(90)
        print("Done.")