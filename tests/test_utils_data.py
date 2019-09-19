import os
import unittest
from .support import TempdirManager
from blurring.utils import WorkFolder


class TestWorkFolder(TempdirManager, unittest.TestCase):

    def create_folder(self, **kwargs):
        tmpdir = self.mkdtemp()
        root = os.path.join(tmpdir, 'test')
        kwargs['root'] = root
        folder = WorkFolder(**kwargs)
        folder.setup()
        return folder

    def test_files(self):
        folder = WorkFolder()
        folder.setup()
        self.assertIsInstance(folder.files('frames'), list)

    def test_full_setup(self):
        folder = WorkFolder()
        self.assertTrue(os.path.exists(folder['root']))
        for dir in folder.FOLDERS:
            self.assertFalse(os.path.exists(folder[dir]))

        folder.setup()
        for dir in folder.FOLDERS:
            self.assertTrue(os.path.exists(folder[dir]))

        self.assertFalse(folder['test'])

    def test_small_setup(self):
        tmpdir = self.mkdtemp()
        root = os.path.join(tmpdir, 'test')
        folder = WorkFolder(root=root)
        self.assertFalse(folder.check(False))

        folder.setup(False)
        self.assertTrue(folder.check(False))
        for dir in folder.FOLDERS:
            self.assertFalse(folder.check(dir))

        folder.setup(['templates', 'cleaned'])
        self.assertFalse(os.path.exists(folder['frames']))
        self.assertTrue(os.path.exists(folder['templates']))
        self.assertTrue(os.path.exists(folder['cleaned']))

        folder.setup('frames')
        self.assertTrue(os.path.exists(folder['frames']))
        self.assertTrue(os.path.exists(folder['templates']))
        self.assertTrue(os.path.exists(folder['cleaned']))

    def test_cleanup_0(self):
        folder = self.create_folder(cleanup=0)
        self.assertTrue(os.path.exists(folder.root))
        folder.clean()
        self.assertTrue(os.path.exists(folder.root))

    def test_cleanup_1(self):
        folder = self.create_folder(cleanup=1)
        self.assertTrue(os.path.exists(folder.root))
        folder.clean()
        self.assertFalse(os.path.exists(folder.root))

    def test_cleanup_2(self):
        folder = self.create_folder(cleanup=2)
        for dir in folder.FOLDERS:
            self.assertTrue(os.path.exists(folder[dir]))
        folder.clean()
        self.assertTrue(os.path.exists(folder.root))
        for dir in folder.FOLDERS:
            self.assertFalse(os.path.exists(folder[dir]))

    def test_exception(self):
        folder = WorkFolder()
        self.assertRaises(TypeError, folder.setup, {'test': False})
        self.assertRaises(TypeError, folder.setup, object())
        self.assertRaises(TypeError, folder.setup, type(2+3j))


if __name__ == '__main__':
    unittest.main()
