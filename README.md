# Gethin's robot wars inspired robot

Here is my design for my custom fighter robot. I am going to create it using a Raspberry pi pico, TT motors, L298N motor drivers, and a servo motor. It will be controlled by a 433mhz radio frequency remote, another raspberry pi pico & a joystick module. The main axe weapon and chassis will be 3d printed in PLA.

It will be powered by AA batteries, the actual robot will be connected using a breadboard & jumper wires, but I want to experiment with a custom PCB for my remote. I will design the PCB in KiCad, also with female sockets so I can remove modules from the remote.

Note: don't quite understand this, but I believe I will need to connect the **grounds** on either side together so they have the same reference point?

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

- Raspberry pi pico 2 WH
- 433 MHz receiver
- 2x L298N motor drivers
- 4x TT motors (raw voltage from L298Ns)
- Metal-geared servo motor
- 6xAA battery pack
- Breadboard
- Jumper wires for wiring
- PLA axe and chassis
- 5V buck converter
