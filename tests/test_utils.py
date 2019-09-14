import os
import unittest
from .support import TempdirManager
from blurring.utils import TempGen


class TestTempGen(TempdirManager, unittest.TestCase):

    def test_create_gen(self):
        tempgen = TempGen(folder='.', data={'test': True})
        self.assertTrue(len(tempgen.folder)>2)
        self.assertIsInstance(tempgen.data, list)
        with self.assertRaises(TypeError):
            TempGen(folder='.', data='')
            TempGen(folder='.', data=[''])

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




if __name__ == '__main__':
    unittest.main()
