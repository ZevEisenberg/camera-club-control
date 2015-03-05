from HardwareInterface import HardwareInterface
from CameraInterface import CameraInterface
from RecordingQuality import RecordingQuality
from HardwareInterface import RecordingLEDState

class CameraClubControl(object):
    def __init__(self):
        # TODO: read from disk
        self.recordingQuality = RecordingQuality.biggest
        self.hw = HardwareInterface(qualityChangeHandler=self)
        self.camera = CameraInterface()

        self.hw.switch_light(RecordingQuality.biggest, True)
        self.hw.switch_light(RecordingQuality.medium, False)
        self.hw.switch_light(RecordingQuality.fastest, False)
        self.hw.recLEDState = RecordingLEDState.off

    def qualityChanged(self, quality):
        if quality is RecordingQuality.biggest:
            self.hw.play_sound(True)
            self.hw.switch_light(RecordingQuality.biggest, True)
            self.hw.switch_light(RecordingQuality.medium, False)
            self.hw.switch_light(RecordingQuality.fastest, False)
            print "low quality"
        elif quality is RecordingQuality.medium:
            self.hw.play_sound(True)
            self.hw.switch_light(RecordingQuality.biggest, False)
            self.hw.switch_light(RecordingQuality.medium, True)
            self.hw.switch_light(RecordingQuality.fastest, False)
            print "mid quality"
        elif quality is RecordingQuality.fastest:
            self.hw.play_sound(True)
            self.hw.switch_light(RecordingQuality.biggest, False)
            self.hw.switch_light(RecordingQuality.medium, False)
            self.hw.switch_light(RecordingQuality.fastest, True)
            print "high quality"

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