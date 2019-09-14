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
