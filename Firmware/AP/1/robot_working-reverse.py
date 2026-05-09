# ===== SAFE MODE (prevents Thonny lockout) =====
# If you plug into USB and open Thonny within 3 seconds,
# the robot code will NOT run, so you can edit files safely.

import time, machine

for i in range(30):  # 30 × 0.1s = 3 seconds
    time.sleep(0.1)
    # If Thonny connects, it interrupts here and gives you REPL access.


# ===== IMPORTS =====
import network
import socket
from machine import Pin, PWM


# ===== LEFT L298N =====
# FL (flip)
FL_EN = PWM(Pin(0))
FL_IN1 = Pin(1, Pin.OUT)
FL_IN2 = Pin(2, Pin.OUT)

# BL (flip)
BL_EN = PWM(Pin(3))
BL_IN1 = Pin(4, Pin.OUT)
BL_IN2 = Pin(5, Pin.OUT)

# ===== RIGHT L298N =====
# FR (normal)
FR_EN = PWM(Pin(6))
FR_IN1 = Pin(7, Pin.OUT)
FR_IN2 = Pin(8, Pin.OUT)

# BR (flip)
BR_EN = PWM(Pin(9))
BR_IN1 = Pin(10, Pin.OUT)
BR_IN2 = Pin(11, Pin.OUT)


# ===== PWM SETUP =====
for pwm in (FL_EN, BL_EN, FR_EN, BR_EN):
    pwm.freq(1000)


# ===== MOTOR DRIVER =====
def drive_motor(en, in1, in2, speed, flipped=False):
    if flipped:
        speed = -speed

    if speed > 0:
        in1.value(1)
        in2.value(0)
        en.duty_u16(int(speed * 65535 / 100))
    elif speed < 0:
        in1.value(0)
        in2.value(1)
        en.duty_u16(int(-speed * 65535 / 100))
    else:
        in1.value(0)
        in2.value(0)
        en.duty_u16(0)

def drive_left(speed):
    drive_motor(FL_EN, FL_IN1, FL_IN2, speed, flipped=True)
    drive_motor(BL_EN, BL_IN1, BL_IN2, speed, flipped=True)

def drive_right(speed):
    drive_motor(FR_EN, FR_IN1, FR_IN2, speed, flipped=False)
    drive_motor(BR_EN, BR_IN1, BR_IN2, speed, flipped=True)



def stop_all():
    drive_left(0)
    drive_right(0)


# ===== WIFI ACCESS POINT =====
ap = network.WLAN(network.AP_IF)
ap.config(essid="Gethin-Robot", password="combat123")
ap.active(True)

print("Robot AP ready at 192.168.4.1")


# ===== UDP RECEIVER =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))
sock.settimeout(0.1)

last_time = time.time()
print("Listening for joystick commands...")


# ===== MAIN LOOP =====
while True:

    # FAILSAFE — stop if no signal for 1 second
    if time.time() - last_time > 1:
        stop_all()

    try:
        data, addr = sock.recvfrom(1024)
        last_time = time.time()

        msg = data.decode().split(",")
        left = int(msg[0])
        right = int(msg[1])

        drive_left(left)
        drive_right(right)

    except:
        pass

