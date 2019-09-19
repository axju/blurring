"""Some nice tools"""
from logging import getLogger
import os
import cv2
import numpy as np


class TempGen():
    """docstring for TempGen."""

    def __init__(self, data, folder='.'):
        self.logger = getLogger(self.__class__.__name__)
        self.folder = os.path.abspath(folder)
        if isinstance(data, dict):
            self.data = [data]
        elif isinstance(data, list):
            self.data = data
        else:
            raise TypeError('The data must be a list or dict!')
        for item in self.data:
            if not isinstance(item, dict):
                raise TypeError('The list should contain only  dict!')

    def create_cv2text(self, name, data):
        """Create a text image with cv2"""
        self.logger.debug('Create cv2text tempalte')
        filename = os.path.join(self.folder, '{}.png'.format(name))
        template = np.zeros((*data['size'], 3), np.uint8)
        cv2.putText(
            template, data['text'], tuple(data['pos']),
            data.get('font', cv2.FONT_HERSHEY_SIMPLEX),
            data['scale'],
            (255, 255, 255), 1)
        cv2.imwrite(filename, template)

    def run(self):
        """create all templates from the data"""
        self.logger.debug('Start template generation')
        for i, data in enumerate(self.data):
            kind = data.get('kind', '')
            name = data.get('name', 'template_{}'.format(i))
            self.logger.debug('Template %i: name="%s", kind="%s"', i, name, kind)
            if kind == 'cv2':
                self.create_cv2text(name, data)
            else:
                self.logger.info('Wrong data. Missing kind definition!')
