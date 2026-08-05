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
    print(f"Starting Motor 2 Nudge & PWM Test on {ROBOT_IP}...")
    print("Keep your hand ready to give Motor 2 a gentle physical nudge if it stalls.\n")

    try:
        # 1. Stop
        print("State: Stopped (servo2=90)")
        send_motor2(90)
        time.sleep(2)

        # 2. Full Speed Burst (The "Nudge" in software form)
        print("State: Full Speed Forward (servo2=180) - Watch if it spins instantly")
        send_motor2(180)
        time.sleep(2)

        # 3. Drop to Low PWM (e.g., 60% speed forward -> ~124)
        print("State: Medium-Low Speed (servo2=124) - Did it keep moving?")
        send_motor2(124)
        time.sleep(3)

        # 4. Drop to Very Low PWM (e.g., just above stop -> ~100)
        print("State: Very Low Speed (servo2=100) - Watch if it stalls out")
        send_motor2(100)
        time.sleep(3)

        # 5. Reverse Full Speed
        print("State: Full Speed Reverse (servo2=0)")
        send_motor2(0)
        time.sleep(2)

        # 6. Stop
        print("State: Stop (servo2=90)")
        send_motor2(90)

        print("\nTest sequence complete.")

    except KeyboardInterrupt:
        print("\n\nTest stopped. Sending safety stop...")
        send_motor2(90)
        print("Done.")