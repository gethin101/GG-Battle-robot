# -------------------------------------------------------------
# 4-WHEEL ROBOT CONTROLLED BY JOYSTICK (MICROPYTHON)
# Matching Gethin's exact wiring + joystick rotated 90° right
# -------------------------------------------------------------

from machine import Pin, PWM, ADC
import time

# -------------------------------------------------------------
# ANALOG JOYSTICK SETUP
# -------------------------------------------------------------
# VRx = GP26 (A0)
# VRy = GP27 (A1)
# Joystick rotated 90° → LEFT = forward, RIGHT = backward
# UP = turn right, DOWN = turn left

x_axis = ADC(26)   # VRx
y_axis = ADC(27)   # VRy

# Dead-zone (medium)
DEADZONE = 0.20

# -------------------------------------------------------------
# MOTOR DRIVER SETUP (L298N LEFT + RIGHT)
# -------------------------------------------------------------
# LEFT L298N pins
ENA_L = PWM(Pin(0))
IN1_L = Pin(1, Pin.OUT)
IN2_L = Pin(2, Pin.OUT)

ENB_L = PWM(Pin(3))
IN3_L = Pin(4, Pin.OUT)
IN4_L = Pin(5, Pin.OUT)

# RIGHT L298N pins
ENA_R = PWM(Pin(6))
IN1_R = Pin(7, Pin.OUT)
IN2_R = Pin(8, Pin.OUT)

ENB_R = PWM(Pin(9))
IN3_R = Pin(10, Pin.OUT)
IN4_R = Pin(11, Pin.OUT)

# Set PWM frequency
ENA_L.freq(1000)
ENB_L.freq(1000)
ENA_R.freq(1000)
ENB_R.freq(1000)

# -------------------------------------------------------------
# REVERSE OPTIONS (in case motors spin wrong)
# -------------------------------------------------------------
reverse_left = False
reverse_right = False

# -------------------------------------------------------------
# HELPER: SET MOTOR SPEED AND DIRECTION
# -------------------------------------------------------------
def drive_motor(pwmA, in1, in2, pwmB, in3, in4, speed, reverse=False):
    """
    Controls BOTH motors on one L298N board.
    speed = -1.0 to +1.0
    reverse = flips direction if motors wired backwards
    """

    if reverse:
        speed = -speed

    # Clamp speed
    if speed > 1: speed = 1
    if speed < -1: speed = -1

    # Convert speed to PWM duty (0–65535)
    duty = int(abs(speed) * 65535)

    if speed > 0:
        # Forward
        in1.value(1)
        in2.value(0)
        in3.value(1)
        in4.value(0)
    elif speed < 0:
        # Backward
        in1.value(0)
        in2.value(1)
        in3.value(0)
        in4.value(1)
    else:
        # Stop
        in1.value(0)
        in2.value(0)
        in3.value(0)
        in4.value(0)

    pwmA.duty_u16(duty)
    pwmB.duty_u16(duty)

# -------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------
while True:

    # Read joystick (0–65535)
    raw_x = x_axis.read_u16()
    raw_y = y_axis.read_u16()

    # Convert to -1.0 to +1.0
    x = (raw_x - 32768) / 32768
    y = (raw_y - 32768) / 32768

    # Apply dead-zone
    if abs(x) < DEADZONE: x = 0
    if abs(y) < DEADZONE: y = 0

    # ---------------------------------------------------------
    # MOVEMENT LOGIC (matching your rotated joystick)
    # ---------------------------------------------------------
    # LEFT  = forward
    # RIGHT = backward
    # UP    = turn right
    # DOWN  = turn left

    forward_back = -x      # LEFT = forward, RIGHT = backward
    turn = y               # UP = right turn, DOWN = left turn

    # Tank turn mixing
    left_speed = forward_back - turn
    right_speed = forward_back + turn

    # Clamp speeds
    left_speed = max(-1, min(1, left_speed))
    right_speed = max(-1, min(1, right_speed))

    # ---------------------------------------------------------
    # SEND SPEEDS TO MOTOR DRIVERS
    # ---------------------------------------------------------
    drive_motor(ENA_L, IN1_L, IN2_L, ENB_L, IN3_L, IN4_L, left_speed, reverse_left)
    drive_motor(ENA_R, IN1_R, IN2_R, ENB_R, IN3_R, IN4_R, right_speed, reverse_right)

    time.sleep(0.01)
