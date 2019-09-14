"""The main module"""
import os
from logging import getLogger
from shutil import copy
from blurring.data import WorkFolder
from blurring.utils import TempGen


class TheBlur():
    """docstring for TheBlur."""

    def __init__(self, **kwargs):
        self.logger = getLogger(self.__class__.__name__)
        self.threshold = kwargs.get('threshold', 0.5)
        self.multi = kwargs.get('multi', True)

        self.work = WorkFolder(**kwargs)
        self.debugdirs = []

    def add_template(self, folder=None, data=None):
        """
        Add a templat to the work folder.
        folder: All images inside the folder.
        data: A file with data to create different templates.
        """
        if folder:
            self.logger.debug('Add template folder "%s"', folder)
            copy(folder, self.work['templates'])
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
