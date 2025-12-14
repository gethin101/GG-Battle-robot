# Gethin's robot wars inspired robot

Here is my design for my custom robot wars inspired battle robot. I am going to create it using a Raspberry pi pico 2 WH, TT motors, L298N motor drivers, and a servo motor. It will be controlled by a 433mhz radio frequency remote, another Raspberry pi pico 2WH, a joystick module and extra control buttons. The main axe weapon and chassis will be 3d printed in PLA.

I will also use a 1.8" SPI LCD Display for the robot to display information on the front of the robot and SK6812 MINI-E RGB leds for the back of the robot. These will both be powered by being plugged into the breadboard in the robot using the pins and jumper wires.

Also I will have sound effects for my robot. I will do this through a PAM8302 amplifier board and 8Ω 2W speaker. The amplifier board will go into the breadboard & the speaker will plug directly into the PAM8302.

It will be powered by AA batteries, the actual robot will be connected using a breadboard & jumper wires, but I want to experiment with a custom PCB for my remote. I will design the PCB in KiCad, also with female sockets so I can remove modules from the remote.

**Note:** don't quite understand this, but I believe I will need to connect the **grounds** on either side together so they have the same reference point?

---

## Control

I will control my robot through the use of the PCB remote which will be in a PLA remote case. There will be a joystick module that with the use of the RF transmitter, will control the TT motors on the robot and therefore the movement of the wheels. 

I will also add a few buttons on the remote, which will control the servo motor which moves the PLA axe weapon and I may make a few of the buttons carry out pre-programmed movement plans or I might add a speaker to the robot and make the buttons send signals to play audio - not sure yet

---
## Components

Here are the lists of components for my robot. I have also made a [full BOM](Components/Bill-Of-Materials.md)
with links to all the parts.

**List of components for remote:**

- Raspberry pi pico 2 WH
- Joystick module
- 433 MHz transmitter
- 2xAA Battery pack
- Custom PCB for joystick, transmitter, microcontroller, battery input & boost converter
- A few buttons for other controls e.g. weapon (possibly)
- I think I will need sockets on my PCB for the microcontroller & joystick
- 5V boost converter

**List of components for robot:**

- Raspberry pi pico 2WH
- 1.8" SPI LCD Display
- SK6812 MINI-E RGBs
- PAM8302 amplifier board
- 8Ω 2W speaker
- 433 MHz receiver
- 2x L298N motor drivers
- 4x TT motors (raw voltage from L298Ns)
- Metal-geared servo motor
- 6xAA battery pack
- Breadboard
- Jumper wires for wiring
- PLA axe and chassis
- 5V buck converter

**I believe my project will cost around £100 so I reckon it will be Tier 3**

---

Remote PCB idea:
- Female headers for the pico and the joystick so they are removable
- Solder on 433 MHz transmitter
- Solder on Boost converter
- Solder on tac buttons
- Solder on battery pack wires

First rough idea for the remote PCB:

<img src="Images/remote_design.png" alt="Alt text" width="700"/>


---

## CircuitPython firmware

- I will need to flash a CircuitPython .uf2 onto my picos
- Install circuitpython libraries .mpys
- Upload the different code.pys to my picos
- Test the firmwares are working


## 📝 License
This project is open-source under the MIT License, was designed during the Hackclub Blueprint project in 2025 and was created by [@gethin101](https://github.com/gethin101)


