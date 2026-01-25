import time

def rf_send(message):
    print("Sending:", message)  

while True:

    rf_send("F")
    time.sleep(1)
