import network
import socket
import time
from machine import Pin, PWM

# ============================
# MOTOR SETUP (your wiring)
# ============================

# LEFT SIDE L298N
L_ENA = PWM(Pin(0))
L_IN1 = Pin(1, Pin.OUT)
L_IN2 = Pin(2, Pin.OUT)
L_ENB = PWM(Pin(3))
L_IN3 = Pin(4, Pin.OUT)
L_IN4 = Pin(5, Pin.OUT)

# RIGHT SIDE L298N
R_ENA = PWM(Pin(6))
R_IN1 = Pin(7, Pin.OUT)
R_IN2 = Pin(8, Pin.OUT)
R_ENB = PWM(Pin(9))
R_IN3 = Pin(10, Pin.OUT)
R_IN4 = Pin(11, Pin.OUT)

# Set PWM frequency
for pwm in [L_ENA, L_ENB, R_ENA, R_ENB]:
    pwm.freq(1000)

# Default speed
speed = 30000

# ============================
# MOTOR CONTROL FUNCTIONS
# ============================

def stop_all():
    global speed
    for pin in [L_IN1, L_IN2, L_IN3, L_IN4, R_IN1, R_IN2, R_IN3, R_IN4]:
        pin.value(0)
    for pwm in [L_ENA, L_ENB, R_ENA, R_ENB]:
        pwm.duty_u16(0)

def forwards():
    L_IN1.value(1); L_IN2.value(0)
    L_IN3.value(1); L_IN4.value(0)
    R_IN1.value(1); R_IN2.value(0)
    R_IN3.value(1); R_IN4.value(0)
    L_ENA.duty_u16(speed); L_ENB.duty_u16(speed)
    R_ENA.duty_u16(speed); R_ENB.duty_u16(speed)

def backwards():
    L_IN1.value(0); L_IN2.value(1)
    L_IN3.value(0); L_IN4.value(1)
    R_IN1.value(0); R_IN2.value(1)
    R_IN3.value(0); R_IN4.value(1)
    L_ENA.duty_u16(speed); L_ENB.duty_u16(speed)
    R_ENA.duty_u16(speed); R_ENB.duty_u16(speed)

def left_turn():
    # Tank turn: left motors reverse, right motors forward
    L_IN1.value(0); L_IN2.value(1)
    L_IN3.value(0); L_IN4.value(1)
    R_IN1.value(1); R_IN2.value(0)
    R_IN3.value(1); R_IN4.value(0)
    L_ENA.duty_u16(speed); L_ENB.duty_u16(speed)
    R_ENA.duty_u16(speed); R_ENB.duty_u16(speed)

def right_turn():
    # Tank turn: right motors reverse, left motors forward
    L_IN1.value(1); L_IN2.value(0)
    L_IN3.value(1); L_IN4.value(0)
    R_IN1.value(0); R_IN2.value(1)
    R_IN3.value(0); R_IN4.value(1)
    L_ENA.duty_u16(speed); L_ENB.duty_u16(speed)
    R_ENA.duty_u16(speed); R_ENB.duty_u16(speed)

# Start stopped
stop_all()

# ============================
# WIFI ACCESS POINT SETUP
# ============================

ap = network.WLAN(network.AP_IF)
ap.config(essid="Gethin-Robot", password="combat123")
ap.active(True)

print("WiFi network created: Gethin-Robot")
print("Password: combat123")
print("Connect and go to: http://192.168.4.1")

# ============================
# HTML PAGE
# ============================

html = """<!DOCTYPE html>
<html>
<head>
<title>Gethin Robot</title>
<style>
body { text-align: center; font-family: Arial; }
button {
  width: 160px; height: 80px;
  font-size: 28px; margin: 10px;
}
select { font-size: 24px; padding: 10px; }
</style>
</head>
<body>
<h1>Gethin Robot Controller</h1>

<button onclick="location.href='/forwards'">FORWARDS</button><br>

<button onclick="location.href='/left'">LEFT</button>
<button onclick="location.href='/stop'">STOP</button>
<button onclick="location.href='/right'">RIGHT</button><br>

<button onclick="location.href='/backwards'">BACKWARDS</button><br><br>

Speed:
<select onchange="location.href='/speed?value=' + this.value">
  <option value="slow">Slow</option>
  <option value="medium" selected>Medium</option>
  <option value="fast">Fast</option>
</select>

</body>
</html>
"""

# ============================
# WEB SERVER + SAFETY STOP
# ============================

last_command_time = time.time()

def safety_check():
    global last_command_time
    if time.time() - last_command_time > 3:
        stop_all()

s = socket.socket()
s.bind(("0.0.0.0", 80))
s.listen(1)

while True:
    safety_check()
    conn, addr = s.accept()
    request = conn.recv(1024).decode()

    last_command_time = time.time()

    if "/forwards" in request:
        forwards()
    elif "/backwards" in request:
        backwards()
    elif "/left" in request:
        left_turn()
    elif "/right" in request:
        right_turn()
    elif "/stop" in request:
        stop_all()
    elif "/speed?value=slow" in request:
        speed = 15000
    elif "/speed?value=medium" in request:
        speed = 30000
    elif "/speed?value=fast" in request:
        speed = 45000

    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send(html)
    conn.close()

