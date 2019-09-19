import os
import unittest
from .support import TempdirManager, DATADIR
from blurring.blur import Blurring


class TestBlurring(TempdirManager, unittest.TestCase):

    VIDEO = os.path.join(DATADIR, 'video.mp4')
    TEMPS = os.path.join(DATADIR, 'template.png')

    def test_run(self):
        out = self.mkdtemp()
        dest = os.path.join(out, 'video.mp4')
        self.assertFalse(os.path.exists(dest))
        blur = Blurring()
        blur.add_template(file=self.TEMPS)
        blur.run(self.VIDEO, dest)
        self.assertTrue(os.path.exists(dest))

    def test_add_template(self):
        templates = self.mkdtemp()
        blur = Blurring()
        blur.add_template(file=self.TEMPS)
        blur.add_template(folder=DATADIR)
        blur.add_template(data={'test': True})

    def test_add_debug(self):
        dir = self.mkdtemp()
        dest = os.path.join(dir, 'test')
        blur = Blurring()
        self.assertFalse(os.path.exists(dest))
        blur.add_debug(dest)
        self.assertTrue(os.path.exists(dest))



if __name__ == '__main__':
    unittest.main()
