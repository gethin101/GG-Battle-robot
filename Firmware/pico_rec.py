
from machine import Pin
import time


IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)

def motor_forward():
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()

def motor_stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()


def rf_receive():

    return "F"  

while True:
    cmd = rf_receive()

    if cmd == "F":
        motor_forward()
    else:
        motor_stop()

    time.sleep(0.1)
