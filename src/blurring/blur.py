"""The main module"""
import os
from logging import getLogger
from shutil import copy, copyfile
import cv2
import numpy as np
from blurring.utils import TempGen, WorkFolder, create_frames, save_frames, find_area


class BlurImage():
    """docstring for BlurImage."""

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


class Blurring():
    """docstring for Blurring."""

    def __init__(self, **kwargs):
        self.logger = getLogger(self.__class__.__name__)

        self.offset = kwargs.get('offset', 30)

        self.blur = BlurImage(**kwargs)
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

    def analyze(self):
        """Analyze the frames and return a list with data"""
        result = []
        for frame_no, frame in enumerate(self.work.files('frames')):
            areas = self.blur.check_image(frame, self.work.files('templates'))
            for area in areas:
                index = find_area(result, area)
                if index == -1:
                    result.append({'area': area, 'frames': [frame_no]})
                else:
                    result[index]['frames'].append(frame_no)

        for values in result:
            sectors = [[values['frames'][0], values['frames'][0]]]
            for index in range(1, len(values['frames'])):
                if (values['frames'][index] - sectors[-1][1]) == 1:
                    sectors[-1][1] = values['frames'][index]
                else:
                    sectors.append([values['frames'][index], values['frames'][index]])
            values['sectors'] = sectors
        return result

    def run(self, src, dest):
        """
        Start the blurring process.
        src: The input video file.
        dist: The blurred output video file.
        """
        self.logger.debug('Start the blurring. src="%s", dest="%s"', src, dest)
        create_frames(src, self.work['frames'])
        data = self.analyze()

        for frame_no, frame in enumerate(self.work.files('frames')):
            basename = os.path.basename(frame)
            areas = []
            for values in data:
                for sector in values['sectors']:
                    if frame_no in range(sector[0]-self.offset, sector[1]+self.offset):
                        areas.append(values['area'])
                        break
            if areas:
                self.blur.blur_image(frame, areas, os.path.join(self.work['cleaned'], basename))
            else:
                copyfile(frame, os.path.join(self.work['cleaned'], basename))
        save_frames(self.work['cleaned'], dest)
