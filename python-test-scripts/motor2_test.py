import time
import urllib.request
import urllib.parse
 
# Replace with your ESP32 robot's actual local IP address
ROBOT_IP = "172.20.10.2"
URL = f"http://{ROBOT_IP}/"
 
def send_command(dtype, data):
    """Sends a POST request to the robot and prints the result."""
    payload = urllib.parse.urlencode({"dtype": dtype, **data}).encode("utf-8")
    try:
        req = urllib.request.Request(URL, data=payload, method="POST")
        with urllib.request.urlopen(req, timeout=3) as response:
            print(f"[SUCCESS] Sent dtype={dtype} {data} -> Status: {response.status}")
    except Exception as e:
        print(f"[ERROR] Failed to send {data}: {e}")
 
if __name__ == "__main__":
    print(f"Starting individual motor & PWM test sequence on {ROBOT_IP}...")
    print("Press Ctrl + C in the terminal to stop.\n")
 
    try:
        while True:
            # 1. Neutral / Stop
            print("State: Both Motors Stopped (90, 90)")
            send_command("speed", {"servo1": 90, "servo2": 90})
            time.sleep(2)
 
            # 2. Motor 1 Full Speed Forward (Motor 2 Stopped)
            print("State: Motor 1 Full Forward (servo1=180, servo2=90)")
            send_command("speed", {"servo1": 180, "servo2": 90})
            time.sleep(2)
 
            # 3. Motor 2 Full Speed Forward (Motor 1 Stopped)
            print("State: Motor 2 Full Forward (servo1=90, servo2=180)")
            send_command("speed", {"servo1": 90, "servo2": 180})
            time.sleep(2)
 
            # 4. Motor 1 PWM / Partial Speed Test (e.g., 75% speed forward)
            print("State: Motor 1 Partial PWM Test (servo1=150, servo2=90)")
            send_command("speed", {"servo1": 150, "servo2": 90})
            time.sleep(2)
 
            # 5. Motor 2 PWM / Partial Speed Test (e.g., 50% speed reverse)
            print("State: Motor 2 Partial PWM Test (servo1=90, servo2=45)")
            send_command("speed", {"servo1": 90, "servo2": 45})
            time.sleep(2)
 
            # --- Kick-start specific tests below ---
            # These stay inside LOW_SPEED_BAND (70-110), which the tests above never touch -
            # steps 2-5 all jump outside that band, so none of them exercise needsKick() at all.
 
            # 6. Motor 1 LOW speed forward from a stop - SHOULD trigger kick
            print("State: Stop, then Motor 1 LOW forward (servo1=100, servo2=90)")
            send_command("speed", {"servo1": 90, "servo2": 90})
            time.sleep(1)
            print("EXPECT: brief full-brightness pulse on Motor 1's PWM LED, then settle dim.")
            send_command("speed", {"servo1": 100, "servo2": 90})
            time.sleep(2)
 
            # 7. Motor 2 LOW speed reverse from a stop - SHOULD trigger kick, opposite direction
            print("State: Stop, then Motor 2 LOW reverse (servo1=90, servo2=75)")
            send_command("speed", {"servo1": 90, "servo2": 90})
            time.sleep(1)
            print("EXPECT: kick pulse again, but Motor 2's REVERSE direction LED lights this time.")
            send_command("speed", {"servo1": 90, "servo2": 75})
            time.sleep(2)
 
            # 8. Boundary check - 110 is exactly at the edge of LOW_SPEED_BAND, should still kick
            print("State: Stop, then Motor 1 at exact kick boundary (servo1=110, servo2=90)")
            send_command("speed", {"servo1": 90, "servo2": 90})
            time.sleep(1)
            print("EXPECT: kick still fires - distanceFromStop == 20, and needsKick() uses <=.")
            send_command("speed", {"servo1": 110, "servo2": 90})
            time.sleep(2)
 
            # 9. Already-moving low speed change - should NOT kick (no stop in between)
            print("State: From 110, straight to 105 with no stop first (servo1=105, servo2=90)")
            print("EXPECT: NO kick pulse - lastSpeed1 was 110, not zeroSpeed, when this was sent.")
            send_command("speed", {"servo1": 105, "servo2": 90})
            time.sleep(2)
 
    except KeyboardInterrupt:
        print("\n\nTest loop stopped. Sending safety stop...")
        send_command("speed", {"servo1": 90, "servo2": 90})
        print("Done.")