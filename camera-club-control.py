import RPi.GPIO as GPIO
import time

# Use board pin numbers instead of GPIO numbers
GPIO.setmode(GPIO.BOARD)

# Pin Numbers
LOW_LED_PIN = 38
MID_LED_PIN = 31
HIGH_LED_PIN = 26
REC_LED_PIN = 15

LOW_BUTTON_PIN = 36
MID_BUTTON_PIN = 29
HIGH_BUTTON_PIN = 24
REC_BUTTON_PIN = 13

SPEAKER_PIN = 7

# Set up pins for input and output
GPIO.setup(LOW_LED_PIN, GPIO.OUT)
GPIO.setup(MID_LED_PIN, GPIO.OUT)
GPIO.setup(HIGH_LED_PIN, GPIO.OUT)
GPIO.setup(REC_LED_PIN, GPIO.OUT)

GPIO.setup(LOW_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(MID_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(HIGH_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(REC_BUTTON_PIN, GPIO.IN, GPIO.PUD_UP)

GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# Set up speaker
SPEAKER_DUTYCYCLE = 50
pwm = GPIO.PWM(SPEAKER_PIN, SPEAKER_DUTYCYCLE)
FREQUENCY_GOOD = 500
FREQUENCY_BAD = 150

recording = False

def switch_light(channel, state):
    value = 0
    if state is True:
        value = 1
    GPIO.output(channel, value)

def handle_button(channel):
    global recording
    if channel is LOW_BUTTON_PIN:
        play_sound(True)
        switch_light(LOW_LED_PIN, True)
        switch_light(MID_LED_PIN, False)
        switch_light(HIGH_LED_PIN, False)
        print "low quality"
    elif channel is MID_BUTTON_PIN:
        play_sound(True)
        switch_light(LOW_LED_PIN, False)
        switch_light(MID_LED_PIN, True)
        switch_light(HIGH_LED_PIN, False)
        print "mid quality"
    elif channel is HIGH_BUTTON_PIN:
        play_sound(True)
        switch_light(LOW_LED_PIN, False)
        switch_light(MID_LED_PIN, False)
        switch_light(HIGH_LED_PIN, True)
        print "high quality"
    elif channel is REC_BUTTON_PIN:
        play_sound(not recording)
        recording = not recording
        switch_light(REC_LED_PIN, recording)
        print "record"

def play_sound(good):
    frequency = None
    if good:
        frequency = FREQUENCY_GOOD
    else:
        frequency = FREQUENCY_BAD

    pwm.ChangeFrequency(frequency)
    pwm.start(SPEAKER_DUTYCYCLE)
    time.sleep(0.25)
    pwm.stop()

def cleanup():
    pwm.stop()
    GPIO.cleanup()
    print "Goodbye"

BOUNCE_TIME = 300
GPIO.add_event_detect(LOW_BUTTON_PIN, GPIO.RISING, callback=handle_button, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(MID_BUTTON_PIN, GPIO.RISING, callback=handle_button, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(HIGH_BUTTON_PIN, GPIO.RISING, callback=handle_button, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(REC_BUTTON_PIN, GPIO.RISING, callback=handle_button, bouncetime=BOUNCE_TIME)

switch_light(LOW_LED_PIN, True)
switch_light(MID_LED_PIN, False)
switch_light(HIGH_LED_PIN, False)
switch_light(REC_LED_PIN, False)

try:
    while True:
        pass
except KeyboardInterrupt:
    cleanup()
