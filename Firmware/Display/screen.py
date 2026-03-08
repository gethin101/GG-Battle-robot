
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_st7735r

class Screen:
    def __init__(self):
    
        displayio.release_displays()

  
        spi = board.SPI() 
        tft_cs = board.GP13
        tft_dc = board.GP14
        tft_rst = board.GP15

        display_bus = displayio.FourWire(
            spi,
            command=tft_dc,
            chip_select=tft_cs,
            reset=tft_rst,
            baudrate=24000000
        )


        self.display = adafruit_st7735r.ST7735R(
            display_bus,
            width=160,
            height=128,
            rotation=90,
            bgr=True
        )


        self.group = displayio.Group()
        self.display.show(self.group)


        self.text_area = label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            x=5,
            y=10
        )
        self.group.append(self.text_area)


    def clear(self, color=0x000000):
        """Fill the screen with a solid colour."""
        bg_bitmap = displayio.Bitmap(self.display.width, self.display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = color

        bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.group = displayio.Group()
        self.group.append(bg_sprite)
        self.display.show(self.group)

 
        self.group.append(self.text_area)

    def write(self, text, x=5, y=10, color=0xFFFFFF):
        """Write text to the screen."""
        self.text_area.text = text
        self.text_area.x = x
        self.text_area.y = y
        self.text_area.color = color

    def status(self, line1="", line2="", line3=""):
        """Convenient multi-line status display."""
        full_text = f"{line1}\n{line2}\n{line3}"
        self.text_area.text = full_text

    def demo(self):
        """Simple demo animation."""
        import time
        colors = [0xFF0000, 0x00FF00, 0x0000FF]

        for c in colors:
            self.clear(c)
            self.write("Robot Ready!", x=20, y=60, color=0xFFFFFF)
            time.sleep(0.8)
