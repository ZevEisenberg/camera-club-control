from HardwareInterface import HardwareInterface
from CameraInterface import CameraInterface
from RecordingQuality import RecordingQuality
from HardwareInterface import RecordingLEDState

class CameraClubControl(object):
    def __init__(self):
        # TODO: read from disk
        self.recordingQuality = RecordingQuality.biggest
        self.hw = HardwareInterface(qualityButtonHandler=self.qualityButtonPressed, recordButtonHandler=self.recordButtonPressed)

        self.hw.switch_light(RecordingQuality.biggest, True)
        self.hw.switch_light(RecordingQuality.medium, False)
        self.hw.switch_light(RecordingQuality.fastest, False)
        self.hw.recLEDState = RecordingLEDState.blinking

        self.camera = CameraInterface()
        self.camera.recording = False

        self.handleQualityChange(self.recordingQuality, user_initiated=False)

    def qualityButtonPressed(self, quality):
        self.handleQualityChange(quality, user_initiated=True)

    def handleQualityChange(self, quality, user_initiated=False):
        print RecordingQuality.string_from_recording_quality(quality)
        if user_initiated:
            self.hw.play_sound(True)

        if quality is RecordingQuality.biggest:
            self.hw.switch_light(RecordingQuality.biggest, True)
            self.hw.switch_light(RecordingQuality.medium, False)
            self.hw.switch_light(RecordingQuality.fastest, False)
        elif quality is RecordingQuality.medium:
            self.hw.switch_light(RecordingQuality.biggest, False)
            self.hw.switch_light(RecordingQuality.medium, True)
            self.hw.switch_light(RecordingQuality.fastest, False)
        elif quality is RecordingQuality.fastest:
            self.hw.switch_light(RecordingQuality.biggest, False)
            self.hw.switch_light(RecordingQuality.medium, False)
            self.hw.switch_light(RecordingQuality.fastest, True)

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
        print "Goodbye"

    def run(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.cleanup()

control = CameraClubControl()
control.run()
