"""The main module"""
from logging import getLogger


class TheBlur():
    """docstring for TheBlur."""

    def __init__(self, **kwargs):
        self.logger = getLogger(self.__class__.__name__)
        self.threshold = kwargs.get('threshold', 0.5)
        self.multi = kwargs.get('multi', True)

    def add_template(self, folder=None, data=None):
        """
        Add a templat to the work folder.
        folder: All images inside the folder.
        data: A file with data to create different templates.
        """
        if folder:
            self.logger.debug('Add template folder "%s"', folder)
        elif data:
            self.logger.debug('Add template data file "%s"', data)

    def add_debug(self, name):
        """Add a debug folder. Only for debugging"""
        self.logger.debug('Add debug folder "%s"', name)

    def run(self, src, dest):
        """
        Start the blurring process.
        src: The input video file.
        dist: The blurred output video file.
        """
        self.logger.debug('Start the blurring. src="%s", dest="%s"', src, dest)
