import time
import board
import pwmio
import busio
import digitalio

from screen import Screen
from led import RobotLEDs
from audio import RobotAudio


left_in1 = digitalio.DigitalInOut(board.GP2)
left_in2 = digitalio.DigitalInOut(board.GP3)
left_pwm = pwmio.PWMOut(board.GP4, frequency=1000)


right_in1 = digitalio.DigitalInOut(board.GP5)
right_in2 = digitalio.DigitalInOut(board.GP6)
right_pwm = pwmio.PWMOut(board.GP7, frequency=1000)

for pin in [left_in1, left_in2, right_in1, right_in2]:
    pin.direction = digitalio.Direction.OUTPUT

def set_motor(left_speed, right_speed):

    def drive(in1, in2, pwm, speed):
        if speed > 0:
            in1.value = True
            in2.value = False
        elif speed < 0:
            in1.value = False
            in2.value = True
        else:
            in1.value = False
            in2.value = False

        pwm.duty_cycle = int(abs(speed) * 655)

    drive(left_in1, left_in2, left_pwm, left_speed)
    drive(right_in1, right_in2, right_pwm, right_speed)
  
weapon_servo = pwmio.PWMOut(board.GP8, frequency=50)

def set_servo(angle):

    pulse = 500 + (angle / 180) * 2000
    duty = int((pulse / 20000) * 65535)
    weapon_servo.duty_cycle = duty

def attack():
    set_servo(0)
    time.sleep(0.15)
    set_servo(90)


rf = busio.UART(board.GP0, board.GP1, baudrate=9600)

def read_rf():
    if rf.in_waiting > 0:
        try:
            raw = rf.readline().decode().strip()
            parts = raw.split(",")
            if len(parts) == 3:
                x = int(parts[0])    
                y = int(parts[1])     
                btn = int(parts[2])    
                return x, y, btn
        except:
            pass
    return None


screen = Screen()
leds = RobotLEDs(pin=board.GP10, count=8)
audio = RobotAudio(pin=board.GP11)


screen.clear(0x000000)
screen.write("Booting robot...", x=10, y=20)
leds.fill((0, 0, 255))
audio.startup_sound()
time.sleep(1)

screen.status("RF: Waiting", "Motors: Idle", "Axe: Safe")
leds.off()



last_speed = 0

while True:
    data = read_rf()

    if data:
        x, y, btn = data


        left = y + x
        right = y - x

  
        left = max(-100, min(100, left))
        right = max(-100, min(100, right))

        set_motor(left, right)

        speed = abs(y)

        if speed == 0 and last_speed > 20:
            leds.braking()
            audio.brake_sound()

        elif speed < 30:
            leds.slowing_down()

        elif speed > 90:
            leds.max_speed()

 
        if btn == 1:
            leds.attack_mode()
            audio.attack_sound()
            attack()

 
        screen.status(
            f"Speed: {speed}",
            f"Turn: {x}",
            "Axe: FIRE" if btn == 1 else "Axe: Ready"
        )

        last_speed = speed

    time.sleep(0.01)
