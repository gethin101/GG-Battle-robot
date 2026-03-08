import time
import board
import busio
import analogio
import digitalio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)


joy_x = analogio.AnalogIn(board.GP26)
joy_y = analogio.AnalogIn(board.GP27)  

def read_joystick():

    x = int(((joy_x.value / 65535) * 200) - 100)
    y = int(((joy_y.value / 65535) * 200) - 100)


    if abs(x) < 5: x = 0
    if abs(y) < 5: y = 0

    return x, y


btn_attack = digitalio.DigitalInOut(board.GP2)
btn_attack.direction = digitalio.Direction.INPUT
btn_attack.pull = digitalio.Pull.UP

def read_buttons():
    return 1 if not btn_attack.value else 0


print("Transmitter Ready")

while True:
    x, y = read_joystick()
    btn = read_buttons()

    packet = f"{x},{y},{btn}\n"
    uart.write(packet.encode())

    time.sleep(0.05)
