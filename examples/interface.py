import os
from blurring.blur import Blurring
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

root = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(root, 'video.mp4')
dest = os.path.join(root, 'blurvideo.mp4')
temp = os.path.join(root, 'test.png')

blur = Blurring(cleanup=1)
blur.add_template(file=temp)
blur.run(src, dest)
