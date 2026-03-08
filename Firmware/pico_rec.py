import time
import board
import busio


uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0.1)

def parse_packet(packet):
    """
    Expected format: "x,y,btn"
    Example: "10,-40,1"
    """
    try:
        parts = packet.split(",")
        if len(parts) != 3:
            return None

        x = int(parts[0])
        y = int(parts[1])
        btn = int(parts[2])

        return x, y, btn
    except:
        return None

print("RF Receiver Ready")

while True:
    if uart.in_waiting > 0:
        try:
            raw = uart.readline().decode().strip()
            data = parse_packet(raw)

            if data:
                x, y, btn = data
                print(f"{x},{y},{btn}")  
        except:
            pass

    time.sleep(0.01)
