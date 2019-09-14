"""Some nice tools"""
from logging import getLogger
import os
import cv2
import numpy as np
import ffmpeg


def create_frames(src, dest, basename='%06d.png'):
    """Extract all frames from a video file."""
    stream = ffmpeg.input(src)
    stream = ffmpeg.output(stream, os.path.join(dest, basename))
    ffmpeg.run(stream, overwrite_output=True, quiet=True)


def save_frames(src, dest, basename='%06d.png'):
    """Create a video file from individual frames"""
    stream = ffmpeg.input(os.path.join(src, basename))
    stream = ffmpeg.output(stream, dest)
    ffmpeg.run(stream, overwrite_output=True, quiet=True)


class TheBlur():
    """docstring for TheBlur."""

    def __init__(self, **kwargs):
        self.logger = getLogger(self.__class__.__name__)
        self.threshold = kwargs.get('threshold', 0.5)
        self.multi = kwargs.get('multi', True)

    def check_image(self, image, temps):
        """Return a list of boundaries"""
        self.logger.debug('Check image "%s"', image)
        _, edges = cv2.threshold(cv2.imread(image, 0), 127, 255, cv2.THRESH_BINARY)

        result = []
        for filename in temps:
            template = cv2.imread(filename, 0)
            width, hight = template.shape[::-1]

            res = cv2.matchTemplate(edges, template, cv2.TM_CCORR_NORMED)
            if self.multi:
                for point in zip(*np.where(res >= self.threshold)[::-1]):
                    result.append((point, (point[0] + width, point[1] + hight)))
            else:
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > self.threshold:
                    result.append((max_loc, (max_loc[0] + width, max_loc[1] + hight)))
        return result

    def blur_image(self, image, areas, dest):
        """Blur all areas on this image"""
        self.logger.debug('blur image "%s"', os.path.basename(image))
        img = cv2.imread(image, 3)
        blurred_img = cv2.GaussianBlur(img, (15, 15), 3)
        mask = np.zeros(img.shape, dtype=np.uint8)
        for point in areas:
            cv2.rectangle(mask, point[0], point[1], (255, 255, 255), -1)
        out = np.where(mask != (255, 255, 255), img, blurred_img)
        if not areas:
            cv2.imwrite(dest, img)
        else:
            cv2.imwrite(dest, out)


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
