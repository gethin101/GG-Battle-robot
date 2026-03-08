import time
import board
import neopixel

class RobotLEDs:
    def __init__(self, pin=board.GP0, count=8, brightness=0.4):
        self.count = count
        self.pixels = neopixel.NeoPixel(
            pin,
            count,
            brightness=brightness,
            auto_write=False
        )

        self.off()


    def fill(self, color):
        for i in range(self.count):
            self.pixels[i] = color
        self.pixels.show()

    def off(self):
        self.fill((0, 0, 0))


    def braking(self):
        """Hard braking = bright red flash."""
        for _ in range(2):
            self.fill((255, 0, 0))
            time.sleep(0.1)
            self.off()
            time.sleep(0.05)
        self.fill((255, 0, 0))

    def slowing_down(self):
        """Soft braking = pulsing orange."""
        for b in range(0, 255, 10):
            self.fill((b, int(b * 0.4), 0))  
            time.sleep(0.02)
        for b in range(255, 0, -10):
            self.fill((b, int(b * 0.4), 0))
            time.sleep(0.02)

    def attack_mode(self):
        """Weapon attack = strobing red/white."""
        for _ in range(6):
            self.fill((255, 0, 0))
            time.sleep(0.05)
            self.fill((255, 255, 255))
            time.sleep(0.05)
        self.fill((255, 0, 0))

    def max_speed(self):
        """Full speed = blue chase animation."""
        for i in range(self.count):
            self.off()
            self.pixels[i] = (0, 0, 255)
            self.pixels.show()
            time.sleep(0.05)
        self.fill((0, 0, 255))
