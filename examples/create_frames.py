import os
from blurring.utils import create_frames

root = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(root, 'video.mp4')
dest = os.path.join(root, 'frames')
create_frames(src, dest)
