"""The wmc integration"""
import os
from blurring import __version__
from blurring.blur import Blurring


def setup(cmd):
    """Only some infos"""
    cmd.__version__ = __version__
    cmd.__help__ = 'Blur the final video'


def main(cmd, **kwargs):
    """Blur the video if you have a templates folder"""
    root = cmd.settings['path']
    src = os.path.join(root, 'full.mp4')
    dest = os.path.join(root, 'full_blur.mp4')
    temp = os.path.join(root, 'templates')

    if not os.path.isdir(temp):
        print('Create a templates folder with the templates to blur! Maybe try:')
        print('>>> blurring-t --help')

    blur = Blurring()
    blur.add_template(folder=temp)
    blur.run(src, dest)
