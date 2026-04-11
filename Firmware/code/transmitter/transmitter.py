from machine import Pin, ADC
import time

tx = Pin(15, Pin.OUT)

x_axis = ADC(26)
y_axis = ADC(27)

# Manchester encoding: each bit becomes two transitions
def manchester_send_bit(bit):
    if bit == 1:
        tx.value(1)
        time.sleep_us(500)
        tx.value(0)
        time.sleep_us(500)
    else:
        tx.value(0)
        time.sleep_us(500)
        tx.value(1)
        time.sleep_us(500)

def send_byte(b):
    # Start bit
    manchester_send_bit(1)

    # 8 data bits
    for i in range(8):
        manchester_send_bit((b >> i) & 1)

    # End bit
    manchester_send_bit(0)

while True:
    x = x_axis.read_u16() >> 6
    y = y_axis.read_u16() >> 6

    if 650 < x < 800 and 650 < y < 800:
        cmd = ord('S')
    elif x < 200:
        cmd = ord('F')
    elif x > 900:
        cmd = ord('B')
    elif y > 900:
        cmd = ord('L')
    elif y < 200:
        cmd = ord('R')
    else:
        cmd = ord('S')

    for _ in range(3):
        send_byte(cmd)

    print("Sent:", chr(cmd))
    time.sleep(0.02)

