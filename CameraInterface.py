from datetime import datetime
from RecordingQuality import RecordingQuality
import os

REC_FOLDER_TEMP = "media/temp"
REC_FOLDER_FINAL = "media/final"

class CameraInterface(object):
    """An abstraction to talk to the camera module"""

    def __init__(self):
        self._recording = False
        self._recording_quality = None

    @staticmethod
    def file_name(quality):
        date_format = '%Y-%m-%d_%H.%M.%S'
        date_string = datetime.now().strftime(date_format)
        quality_string = RecordingQuality.string_from_recording_quality(quality, human_readable=False)
        extension = 'h264'
        filename = '{0}_{1}.{2}'.format(date_string, quality_string, extension)
        return filename

    @staticmethod
    def file_path(filename, temp):
        prefix = REC_FOLDER_TEMP if temp else REC_FOLDER_FINAL
        path = os.path.join(prefix, filename)
        return path

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
                file_name = CameraInterface.file_name(self.recording_quality)
                file_path = CameraInterface.file_path(file_name, temp=True)
                print "starting recording to file {0}".format(file_path)
                # start recording
            else:
                print "stopping recording"
                # stop recording and move file


    @property
    def recording_quality(self):
        """The recording quality"""
        return self._recording_quality

    @recording_quality.setter
    def recording_quality(self, value):
        """The recording quality of the camera"""
        self._recording_quality = value
