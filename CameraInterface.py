import time
from RecordingQuality import RecordingQuality

class CameraInterface(object):
    """An abstraction to talk to the camera module"""

    def __init__(self):
        self._recording = False
        self._recordingQuality = None

    @property
    def recording(self):
        """Whether the camera is recording"""
        return self._recording

    @recording.setter
    def recording(self, value):
        """Whether the camera is currently recording"""
        if value is not self._recording:
            self._recording = value
            if value is True:
                print "starting recording"
                # start recording
            else:
                print "stopping recording"
                # stop recording and move file


    @property
    def recordingQuality(self):
        """The recording quality"""
        return self._recordingQuality

    @recordingQuality.setter
    def recordingQuality(self, value):
        """The recording quality of the camera"""
