import os
import filecmp
import unittest
from .support import TempdirManager, DATADIR
from blurring.blur import BlurImage
from blurring.utils import TempGen, create_frames, save_frames


class TestFrames(TempdirManager, unittest.TestCase):

    def test_create_save_frames(self):
        dest = self.mkdtemp()
        self.assertFalse(os.listdir(dest))
        create_frames(os.path.join(DATADIR, 'video.mp4'), dest)
        self.assertTrue(os.listdir(dest))
        filename = os.path.join(dest, 'video.mp4')
        self.assertFalse(os.path.exists(filename))
        save_frames(dest, filename)


class TestBlurImage(TempdirManager, unittest.TestCase):

    FILENAME1 = os.path.join(DATADIR, 'frame000001.png')
    FILENAME2 = os.path.join(DATADIR, 'frame000002.png')
    TEMPS = [os.path.join(DATADIR, 'template.png')]

    def test_check_image(self):
        blur = BlurImage(multi=False)
        self.assertFalse(blur.check_image(self.FILENAME1, self.TEMPS))
        self.assertTrue(blur.check_image(self.FILENAME2, self.TEMPS))

    def test_check_image_multi(self):
        blur = BlurImage(multi=True)
        self.assertFalse(blur.check_image(self.FILENAME1, self.TEMPS))
        self.assertTrue(blur.check_image(self.FILENAME2, self.TEMPS))

    def test_blur_image(self):
        root = self.mkdtemp()
        blur = BlurImage()
        file1 = os.path.join(root, 'frame000001.png')
        area1 = blur.check_image(self.FILENAME1, self.TEMPS)
        blur.blur_image(self.FILENAME1, area1, file1)
        self.assertTrue(filecmp.cmp(self.FILENAME1, file1))

        file2 = os.path.join(root, 'frame000002.png')
        area2 = blur.check_image(self.FILENAME2, self.TEMPS)
        print(area2)
        blur.blur_image(self.FILENAME2, area2, file2)
        self.assertFalse(filecmp.cmp(self.FILENAME2, file2))


class TestTempGen(TempdirManager, unittest.TestCase):

    def test_create_gen(self):
        tempgen = TempGen(folder='.', data={'test': True})
        self.assertTrue(len(tempgen.folder)>2)
        self.assertIsInstance(tempgen.data, list)
        with self.assertRaises(TypeError):
            TempGen(folder='.', data='')

        with self.assertRaises(TypeError):
            TempGen(folder='.', data=[''])

        tempgen = TempGen(folder='.', data=[{'test': True}])
        self.assertIsInstance(tempgen.data, list)

    def test_create_temp_cv2(self):
        folder = self.mkdtemp()
        data = {
            'kind': 'cv2',
            'name': 'test',
            'size': [18, 70],
            'text': 'PASSWORD',
            'scale': 0.4,
            'font': 0,
            'pos': [0, 12],
        }
        self.assertFalse(os.path.exists(os.path.join(folder, 'test.png')))
        TempGen(folder=folder, data=data).run()
        self.assertTrue(os.path.exists(os.path.join(folder, 'test.png')))

    def test_run_logging(self):
        data = {}
        with self.assertLogs('TempGen', level='INFO') as cm:
            TempGen(data=data).run()
            self.assertEqual(cm.output, ['INFO:TempGen:Wrong data. Missing kind definition!'])




if __name__ == '__main__':
    unittest.main()
