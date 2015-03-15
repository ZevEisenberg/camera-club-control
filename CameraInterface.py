from datetime import datetime
import picamera
from RecordingQuality import RecordingQuality
import os

REC_FOLDER_TEMP = "media/temp"
REC_FOLDER_FINAL = "media/final"

class CurrentlyRecordingError(ValueError):
    pass

class CameraInterface(object):
    """An abstraction to talk to the camera module"""

    def __init__(self):
        self._recording = False
        # TODO: read from disk
        self._recording_quality = RecordingQuality.biggest
        self.current_file_name = None
        self.camera = picamera.PiCamera()

    @staticmethod
    def file_name(quality):
        date_format = '%Y-%m-%d_%H.%M.%S.%f'
         # %f prints microseconds, to trim off 3 digits to print truncated miliseconds
        date_string = datetime.now().strftime(date_format)[:-3]
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
    def recording(self, recording):
        """Whether the camera is currently recording"""
        if recording is not self._recording:
            self._recording = recording
            if recording is True:
                file_name = CameraInterface.file_name(self.recording_quality)
                self.current_file_name = file_name

                self.camera.resolution = RecordingQuality.resolution(self.recording_quality)
                self.camera.framerate = RecordingQuality.framerate(self.recording_quality)

                temp_path = CameraInterface.file_path(self.current_file_name, temp=True)
                self.camera.start_recording(temp_path)
            else:
                self.camera.stop_recording()
                temp_path = CameraInterface.file_path(self.current_file_name, temp=True)
                final_path = CameraInterface.file_path(self.current_file_name, temp=False)
                os.rename(temp_path, final_path)
                self.current_file_name = None
                # stop_recording() may throw errors, which we need to catch


    @property
    def recording_quality(self):
        """The recording quality"""
        return self._recording_quality

    @recording_quality.setter
    def recording_quality(self, quality):
        """The recording quality. Raises a CurrentlyRecordingError if you attempt to set the quality while the camera is recording"""
        if self.recording:
            raise CurrentlyRecordingError()
        else:
            self._recording_quality = quality
