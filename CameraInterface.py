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
        self._recording = value
    
    @property
    def recordingQuality(self):
        """The recording quality"""
        return self._recordingQuality
    
    @recordingQuality.setter
    def recordingQuality(self, value):
        """The recording quality of the camera"""