from HardwareInterface import HardwareInterface
from CameraInterface import CameraInterface, CurrentlyRecordingError
from RecordingQuality import RecordingQuality
from HardwareInterface import RecordingLEDState

class CameraClubControl(object):
    def __init__(self):
        self.hw = HardwareInterface(qualityButtonHandler=self.qualityButtonPressed, recordButtonHandler=self.recordButtonPressed)

        self.hw.switch_light(RecordingQuality.biggest, True)
        self.hw.switch_light(RecordingQuality.medium, False)
        self.hw.switch_light(RecordingQuality.fastest, False)
        self.hw.recLEDState = RecordingLEDState.blinking

        self.camera = CameraInterface()

        self.handleQualityChange(self.camera.recording_quality, user_initiated=False)

    def qualityButtonPressed(self, quality):
        self.handleQualityChange(quality, user_initiated=True)

    def handleQualityChange(self, quality, user_initiated=False):
        try:
            self.camera.recording_quality = quality
        except CurrentlyRecordingError:
            if user_initiated:
                self.hw.play_sound(False)
                print "TODO: flash REC light rapidly"
        else:
            self.hw.recording_quality = quality
            if user_initiated:
                self.hw.play_sound(True)

    def recordButtonPressed(self):
        rec_state = self.camera.recording
        if rec_state is True:
            self.camera.recording = False
            self.hw.recLEDState = RecordingLEDState.blinking
            self.hw.play_sound(False)
        else:
            self.camera.recording = True
            self.hw.recLEDState = RecordingLEDState.on
            self.hw.play_sound(True)

    def cleanup(self):
        self.hw.cleanup()
        print "WARNING: remember to clean up the current recording here."
        print "Goodbye"

    def run(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.cleanup()

control = CameraClubControl()
control.run()
