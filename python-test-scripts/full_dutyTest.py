import time
import urllib.request
import urllib.parse

# Replace with your ESP32 robot's actual local IP address
ROBOT_IP = "172.20.10.2"
URL = f"http://{ROBOT_IP}/"

def send_motors(servo1_val, servo2_val):
    """Sends binary speed commands to both motors."""
    payload = urllib.parse.urlencode({"dtype": "speed", "servo1": servo1_val, "servo2": servo2_val}).encode("utf-8")
    try:
        req = urllib.request.Request(URL, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=3) as response:
            print(f"[SUCCESS] Motors set -> Motor 1: {servo1_val}, Motor 2: {servo2_val} | Status: {response.status}")
    except Exception as e:
        print(f"[ERROR] Failed to send motors: {e}")

if __name__ == "__main__":
    print(f"Starting Full Stop / 100% Binary Drive Test on {ROBOT_IP}...\n")

    try:
        # 1. Stop
        print("State: Stop (90, 90)")
        send_motors(90, 90)
        time.sleep(1)

        # 2. Both Forward at 100%
        print("State: Both 100% Forward (0, 180)")
        send_motors(0, 180)
        time.sleep(0.2)

        # 3. Stop
        print("State: Stop (90, 90)")
        send_motors(90, 90)
        time.sleep(1)

        # 4. Both Reverse at 100%
        print("State: Both 100% Reverse (180, 0)")
        send_motors(180, 0)
        time.sleep(0.2)

        # 5. Spin Turn (Left forward, Right reverse)
        print("State: Spin Turn - Left Forward, Right Reverse (0, 0)")
        send_motors(0, 0)
        time.sleep(0.2)
        # 6. Final Stop
        print("State: Final Stop (90, 90)")
        send_motors(90, 90)

        print("\nTest sequence complete.")

    except KeyboardInterrupt:
        print("\n\nTest stopped. Sending safety stop...")
        send_motors(90, 90)
        print("Done.")