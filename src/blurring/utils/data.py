"""Dealing with data"""
import os
from logging import getLogger
from tempfile import mkdtemp
from shutil import rmtree


class WorkFolder():
    """docstring for WorkFolder."""

    FOLDERS = ['frames', 'cleaned', 'templates']

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

    def _get_dirs_arg(self, dirs):
        if isinstance(dirs, str):
            dirs = [dirs]
        elif isinstance(dirs, (int, float)):
            if dirs:
                dirs = [name for name in self.subdirs]
            else:
                dirs = []
        if not isinstance(dirs, list):
            raise TypeError('"dirs" must be of type list, str or bool!')
        return dirs

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

        dirs = self._get_dirs_arg(dirs)
        for name in dirs:
            if not os.path.exists(self[name]):
                os.makedirs(self[name])
                self.logger.debug('Create directory "%s"', self.subdirs[name])

    def check(self, dirs=True):
        """
        Check the work folder
        dirs=False -> Check only the work folder
        dirs=True -> Check work folder and all subfolder
        dirs='frames' -> Check work folder and "frames" subfolder
        dirs=['frames', 'templates'] -> Check work folder, "frames" and "templates" subfolder
        """
        if not os.path.exists(self.root):
            return False
        dirs = self._get_dirs_arg(dirs)
        for name in dirs:
            if not os.path.exists(self[name]):
                return False
        return True

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

    def files(self, kind):
        """Return a list with all fils in the subdirectory"""
        return sorted([os.path.join(self.subdirs[kind], fn) for fn in os.listdir(self.subdirs[kind])])
