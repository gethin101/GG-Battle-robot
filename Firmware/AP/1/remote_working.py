from machine import ADC, Pin
import network
import socket
import time

# Joystick pins
x = ADC(26)
y = ADC(27)
sw = Pin(16, Pin.IN, Pin.PULL_UP)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("Gethin-Robot", "combat123")

print("Connecting to robot...")
while not sta.isconnected():
    time.sleep(0.1)

print("Connected! My IP:", sta.ifconfig()[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
robot_ip = "192.168.4.1"
port = 5005

def map_axis(val):
    return int((val - 32768) / 32768 * 100)

while True:
    x_val = x.read_u16()
    y_val = y.read_u16()

    forward = map_axis(y_val)
    turn = map_axis(x_val)

    left = forward + turn
    right = forward - turn

    left = max(-100, min(100, left))
    right = max(-100, min(100, right))

    button = 0 if sw.value() == 0 else 1

    msg = f"{left},{right},{button}"
    sock.sendto(msg.encode(), (robot_ip, port))

    time.sleep(0.05)

