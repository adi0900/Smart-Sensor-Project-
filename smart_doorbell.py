from gpiozero import MotionSensor, LED, Buzzer, Button
from datetime import datetime
import os
import time

# Initialize components (GPIO pins)
pir = MotionSensor(17)
button = Button(23)
led = LED(27)
buzzer = Buzzer(22)

# Log file directory
LOG_DIR = "/home/pi/visitor_log"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "visitors.txt")

def log_visitor():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"Visitor detected and rang doorbell at {timestamp}\n")
    print(f"[LOG] Visitor entry logged at {timestamp}")

def ring_doorbell():
    print("[DOORBELL] Button pressed! Ringing doorbell...")
    for _ in range(3):  # Ring buzzer and blink LED 3 times
        buzzer.on()
        led.on()
        time.sleep(0.2)
        buzzer.off()
        led.off()
        time.sleep(0.2)

print("[SYSTEM] Smart Doorbell is active...")

try:
    while True:
        print("[SYSTEM] Waiting for visitor motion...")
        pir.wait_for_motion()
        print("[INFO] Visitor detected. Awaiting button press...")

        button.wait_for_press()
        ring_doorbell()
        log_visitor()

        print("[INFO] Cycle complete. Resetting system...")

except KeyboardInterrupt:
    print("\n[SYSTEM] Shutting down smart doorbell.")
finally:
    led.off()
    buzzer.off()