import time
import board

try:
    import audiopwmio as audioio
except ImportError:
    import audioio

from audiocore import WaveFile

class RobotAudio:
    def __init__(self, pin=board.GP1):

        self.audio = audioio.AudioOut(pin)


    def play_wav(self, filename, wait=True):
        """Play a .wav file stored on the Pico."""
        try:
            with open(filename, "rb") as f:
                wav = WaveFile(f)
                self.audio.play(wav)
                if wait:
                    while self.audio.playing:
                        pass
        except OSError:
            print("Audio file not found:", filename)

    def beep(self, freq=800, duration=0.1):
        """Simple square-wave beep for movement or UI feedback."""
        import math
        import array

        length = 100
        sine_wave = array.array("H", [0] * length)
        for i in range(length):
            sine_wave[i] = int((math.sin(i / length * 2 * math.pi) * 0.5 + 0.5) * 65535)

        sample = audioio.RawSample(sine_wave, sample_rate=freq * length)
        self.audio.play(sample, loop=True)
        time.sleep(duration)
        self.audio.stop()


    def attack_sound(self):
        """Plays a sharp attack sound."""
        self.play_wav("attack.wav")

    def brake_sound(self):
        """Short descending beep for braking."""
        for f in range(1200, 400, -200):
            self.beep(freq=f, duration=0.05)

    def startup_sound(self):
        """Robot boot-up jingle."""
        for f in [400, 600, 900, 1200]:
            self.beep(freq=f, duration=0.08)

    def error_sound(self):
        """Low warning tone."""
        self.beep(freq=200, duration=0.4)
