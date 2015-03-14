# sudo pip install enum34
from enum import Enum

class RecordingQuality(Enum):
    biggest = 1 # 1920x1080@30
    medium = 2 # 1280x720@49
    fastest = 3 # 640x480@90

    def string_from_recording_quality(quality):
        multiplication_sign = '\xC3\x97'
        lookup = {
            RecordingQuality.biggest: 'Biggest: 1920{0}1080 @ 30 fps'.format(multiplication_sign),
            RecordingQuality.medium: 'Medium: 1280{0}720 @ 49 fps'.format(multiplication_sign),
            RecordingQuality.fastest: 'Fastest: 640{0}480 @ 90 fps'.format(multiplication_sign)
        }
        return lookup[quality]
