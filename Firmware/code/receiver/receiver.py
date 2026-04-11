from machine import Pin, PWM
import time

rx = Pin(14, Pin.IN)

# -------------------------------------------------------------
# Manchester decode
# -------------------------------------------------------------
def read_manchester_bit():
    first = rx.value()
    time.sleep_us(500)
    second = rx.value()
    time.sleep_us(500)

    if first == 1 and second == 0:
        return 1
    if first == 0 and second == 1:
        return 0
    return None  # noise

def read_byte():
    # Wait for start bit (1)
    while True:
        b = read_manchester_bit()
        if b == 1:
            break

    val = 0
    for i in range(8):
        bit = None
        while bit is None:
            bit = read_manchester_bit()
        val |= (bit << i)

    # End bit
    read_manchester_bit()
    return val

# -------------------------------------------------------------
# MOTOR DRIVER SETUP (your exact wiring)
# -------------------------------------------------------------
ENA_L = PWM(Pin(0));  IN1_L = Pin(1, Pin.OUT); IN2_L = Pin(2, Pin.OUT)
ENB_L = PWM(Pin(3));  IN3_L = Pin(4, Pin.OUT); IN4_L = Pin(5, Pin.OUT)

ENA_R = PWM(Pin(6));  IN1_R = Pin(7, Pin.OUT); IN2_R = Pin(8, Pin.OUT)
ENB_R = PWM(Pin(9));  IN3_R = Pin(10, Pin.OUT); IN4_R = Pin(11, Pin.OUT)

for pwm in [ENA_L, ENB_L, ENA_R, ENB_R]:
    pwm.freq(1000)

def drive_motor(pwmA, in1, in2, pwmB, in3, in4, speed):
    speed = max(-1, min(1, speed))
    duty = int(abs(speed) * 65535)

    if speed > 0:
        in1.value(1); in2.value(0)
        in3.value(1); in4.value(0)
    elif speed < 0:
        in1.value(0); in2.value(1)
        in3.value(0); in4.value(1)
    else:
        in1.value(0); in2.value(0)
        in3.value(0); in4.value(0)

    pwmA.duty_u16(duty)
    pwmB.duty_u16(duty)

# -------------------------------------------------------------
# SAFE MAIN LOOP — only runs when you call run()
# -------------------------------------------------------------
def run():
    print("Receiver running… Press STOP to exit safely.")
    last_cmd = 'S'
    last_time = time.ticks_ms()

    while True:
        try:
            b = read_byte()
            c = chr(b)

            if c in ['F','B','L','R','S']:
                last_cmd = c
                last_time = time.ticks_ms()

        except:
            pass

        if time.ticks_diff(time.ticks_ms(), last_time) > 500:
            last_cmd = 'S'

        if last_cmd == 'F':
            L, R = 1, 1
        elif last_cmd == 'B':
            L, R = -1, -1
        elif last_cmd == 'L':
            L, R = -1, 1
        elif last_cmd == 'R':
            L, R = 1, -1
        else:
            L, R = 0, 0

        drive_motor(ENA_L, IN1_L, IN2_L, ENB_L, IN3_L, IN4_L, L)
        drive_motor(ENA_R, IN1_R, IN2_R, ENB_R, IN3_R, IN4_R, R)

        time.sleep(0.01)

