"""Dealing with data"""
import os
from logging import getLogger
from tempfile import mkdtemp
from shutil import rmtree


class WorkFolder():
    """docstring for WorkFolder."""

    FOLDERS = ['frames', 'templates', 'cleaned']

    def __init__(self, **kwargs):
        """
        root: The work folder. Create temp folder if not used.
        cleanup: 0=nothing, 1=folder, 2=files+subfolder
        """
        self.logger = getLogger(self.__class__.__name__)
        self.logger.debug('Create WorkFolder object')

        self.cleanup = kwargs.get('cleanup', 1)
        self.root = kwargs.get('root', mkdtemp())
        self.subdirs = {name: os.path.join(self.root, name) for name in self.FOLDERS}

    def __del__(self):
        self.clean()

    def __getitem__(self, key):
        if key == 'root':
            return self.root
        if key in self.subdirs:
            return self.subdirs[key]
        return None

    def setup(self, dirs=True):
        """
        Setup work folder
        dirs=False -> Create only the work folder
        dirs=True -> Create work folder and all subfolder
        dirs='frames' -> Create work folder and "frames" subfolder
        dirs=['frames', 'templates'] -> Create work folder, "frames" and "templates" subfolder
        """
        if not os.path.exists(self.root):
            os.makedirs(self.root)
            self.logger.debug('Create directory "%s"', self.root)

        if isinstance(dirs, str):
            dirs = [dirs]
        elif isinstance(dirs, (int, float)):
            if dirs:
                dirs = [name for name in self.subdirs]
            else:
                dirs = []

        if not isinstance(dirs, list):
            raise TypeError('"dirs" must be of type list, str or bool!')
        for name in dirs:
            if not os.path.exists(self[name]):
                os.makedirs(self[name])
                self.logger.debug('Create directory "%s"', self.subdirs[name])

    def clean(self):
        """
        Delete the work folder (cleanup==1) or subfolders(cleanup==2).
        Skip the cleaning of cleanup==0.
        """
        if self.cleanup == 1:
            if os.path.exists(self.root):
                rmtree(self.root)
                self.logger.debug('Delete directory"%s"', self.root)
        elif self.cleanup == 2:
            for name in os.listdir(self.root):
                rmtree(os.path.join(self.root, name))
