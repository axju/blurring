import os
from blurring.utils import TempGen
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

folder = os.path.dirname(__file__)
data = [
    {
        'kind': 'cv2',
        'name': 'test',
        'size': [18, 70],
        'text': 'PASSWORD',
        'scale': 0.4,
        'font': 0,
        'pos': [0, 12],
    }
]
tempgen = TempGen(folder=folder, data=data)
tempgen.run()
