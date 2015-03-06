# sudo pip install enum34
from enum import Enum

class RecordingQuality(Enum):
    biggest = 1 # 1920x1080@30
    medium = 2 # 1280x720@49
    fastest = 3 # 640x480@90
