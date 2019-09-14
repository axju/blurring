"""The main module"""
import os
from logging import getLogger
from shutil import copy, copyfile
from blurring.data import WorkFolder
from blurring.utils import TempGen, TheBlur, create_frames, save_frames


class Interface():
    """docstring for TheBlur."""

    def __init__(self, **kwargs):
        self.logger = getLogger(self.__class__.__name__)

        self.blur = TheBlur(**kwargs)
        self.work = WorkFolder(**kwargs)
        self.debugdirs = []

        if kwargs.get('setup', True):
            self.work.setup()

    def add_template(self, file=None, folder=None, data=None):
        """
        Add a templat to the work folder.
        file: Add a image file.
        folder: All images inside the folder.
        data: A file with data to create different templates.
        """
        if file:
            self.logger.debug('Add template file "%s"', file)
            copyfile(file, os.path.join(self.work['templates'], os.path.basename(file)))
        elif folder:
            self.logger.debug('Add template folder "%s"', folder)
            for name in os.listdir(folder):
                filename = os.path.join(folder, name)
                if os.path.isfile(filename):
                    copy(filename, os.path.join(self.work['templates'], name))
        elif data:
            self.logger.debug('Add template data file "%s"', data)
            TempGen(folder=self.work['templates'], data=data).run()

    def add_debug(self, name):
        """Add a debug folder. Only for debugging"""
        foldername = os.path.abspath(name)
        self.logger.debug('Add debug folder "%s"', foldername)
        self.debugdirs.append(foldername)
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            self.logger.debug('Create debug folder "%s"', foldername)

    def run(self, src, dest):
        """
        Start the blurring process.
        src: The input video file.
        dist: The blurred output video file.
        """
        self.logger.debug('Start the blurring. src="%s", dest="%s"', src, dest)
        create_frames(src, self.work['frames'])
        for frame in self.work.files('frames'):
            basename = os.path.basename(frame)
            areas = self.blur.check_image(frame, self.work.files('templates'))
            if areas:
                self.blur.blur_image(frame, areas, os.path.join(self.work['cleaned'], basename))
            else:
                copyfile(frame, os.path.join(self.work['cleaned'], basename))
        save_frames(self.work['cleaned'], dest)
