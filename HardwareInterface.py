import RPi.GPIO as GPIO
import threading
import time
from RecordingQuality import RecordingQuality

# sudo pip install enum34
from enum import Enum

class RecordingLEDState(Enum):
    off = 1
    on = 2
    blinking = 3

# Minimum time, in milliseconds, between two buton presses for them to register as two separate presses
BOUNCE_TIME = 300

# Duration, in seconds, of recording light blinking
REC_BLINK_TIME = 0.4

# Pin Number Constants
BIG_LED_PIN = 38
MED_LED_PIN = 31
FAST_LED_PIN = 26
REC_LED_PIN = 15

BIG_BUTTON_PIN = 36
MED_BUTTON_PIN = 29
FAST_BUTTON_PIN = 24
REC_BUTTON_PIN = 13

SPEAKER_PIN = 7

# Speaker Constants
SPEAKER_DUTYCYCLE = 50
FREQUENCY_GOOD = 500
FREQUENCY_BAD = 150
BEEP_DURATION = 0.25

class HardwareInterface(object):
    """An abstraction to talk to the camera club hardware user interface"""

    def __init__(self, qualityButtonHandler, recordButtonHandler):
        self.configure_GPIO()
        self._recLEDState = None
        self.pwm = GPIO.PWM(SPEAKER_PIN, SPEAKER_DUTYCYCLE)
        self.qualityButtonHandler = qualityButtonHandler
        self.recordButtonHandler = recordButtonHandler

    def cleanup(self):
        self.pwm.stop()
        self.recLEDState = RecordingLEDState.off
        GPIO.cleanup()

    def play_sound(self, good):
        frequency = FREQUENCY_GOOD if good else FREQUENCY_BAD

        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(SPEAKER_DUTYCYCLE)
        time.sleep(BEEP_DURATION)
        self.pwm.stop()

    def switch_light(self, quality, state):
        channel = None
        if quality is RecordingQuality.biggest:
            channel = BIG_LED_PIN
        elif quality is RecordingQuality.medium:
            channel = MED_LED_PIN
        elif quality is RecordingQuality.fastest:
            channel = FAST_LED_PIN
        else:
            raise ValueError("Unknown recording quality specified")

        if channel:
            GPIO.output(channel, 1 if state else 0)

    def blink_rec_light(self):
        t = threading.Thread(target=self.blink_rec_on)
        t.start()

    def blink_rec_on(self):
        if self.recLEDState is RecordingLEDState.blinking:
            GPIO.output(REC_LED_PIN, 1)
            time.sleep(REC_BLINK_TIME)
            t = threading.Thread(target=self.blink_rec_off)
            t.start()

    def blink_rec_off(self):
        if self.recLEDState is RecordingLEDState.blinking:
            GPIO.output(REC_LED_PIN, 0)
            time.sleep(REC_BLINK_TIME)
            t = threading.Thread(target=self.blink_rec_on)
            t.start()

    def handle_quality_button(self, channel):
        quality = None
        if channel is BIG_BUTTON_PIN:
            quality = RecordingQuality.biggest
        elif channel is MED_BUTTON_PIN:
            quality = RecordingQuality.medium
        elif channel is FAST_BUTTON_PIN:
            quality = RecordingQuality.fastest
        else:
            raise RuntimeError("Unknown button pushed on channel %d" % (channel))
        if quality:
            self.qualityButtonHandler(quality)

    def handle_record_button(self, channel):
        self.recordButtonHandler()

    def configure_GPIO(self):
        """Bind GPIO pins for inputs and outputs"""

        # Use board pin numbers instead of GPIO numbers
        GPIO.setmode(GPIO.BOARD)

        # Set up LED pins for output
        GPIO.setup(BIG_LED_PIN, GPIO.OUT)
        GPIO.setup(MED_LED_PIN, GPIO.OUT)
        GPIO.setup(FAST_LED_PIN, GPIO.OUT)
        GPIO.setup(REC_LED_PIN, GPIO.OUT)

        # Set up LED button pins for input
        GPIO.setup(BIG_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(MED_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(FAST_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(REC_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)

        # Set up speaker
        GPIO.setup(SPEAKER_PIN, GPIO.OUT)

        # Set up button handler functions
        GPIO.add_event_detect(BIG_BUTTON_PIN, GPIO.RISING, callback=self.handle_quality_button, bouncetime=BOUNCE_TIME)
        GPIO.add_event_detect(MED_BUTTON_PIN, GPIO.RISING, callback=self.handle_quality_button, bouncetime=BOUNCE_TIME)
        GPIO.add_event_detect(FAST_BUTTON_PIN, GPIO.RISING, callback=self.handle_quality_button, bouncetime=BOUNCE_TIME)
        GPIO.add_event_detect(REC_BUTTON_PIN, GPIO.RISING, callback=self.handle_record_button, bouncetime=BOUNCE_TIME)

    @property
    def recLEDState(self):
        """The state of the recording LED"""
        return self._recLEDState

    @recLEDState.setter
    def recLEDState(self, value):
        self._recLEDState = value
        if value is RecordingLEDState.off:
            GPIO.output(REC_LED_PIN, 0)
        elif value is RecordingLEDState.on:
            GPIO.output(REC_LED_PIN, 1)
        elif value is RecordingLEDState.blinking:
            self.blink_rec_light()
        else:
            raise ValueError("Unknown recording LED state")
