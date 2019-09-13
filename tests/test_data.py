import os
import unittest
import tempfile
import shutil
from blurring.data import WorkFolder


class TempdirManager(object):

    def setUp(self):
        super().setUp()
        self.tempdirs = []

    def tearDown(self):
        super().tearDown()
        while self.tempdirs:
            shutil.rmtree(self.tempdirs.pop())

    def mkdtemp(self):
        self.tempdirs.append(tempfile.mkdtemp())
        return self.tempdirs[-1]


class TestWorkFolder(TempdirManager, unittest.TestCase):

    def create_folder(self, **kwargs):
        tmpdir = self.mkdtemp()
        root = os.path.join(tmpdir, 'test')
        kwargs['root'] = root
        folder = WorkFolder(**kwargs)
        folder.setup()
        return folder

    def test_full_setup(self):
        folder = WorkFolder()
        self.assertTrue(os.path.exists(folder.root))
        for dir in folder.FOLDERS:
            self.assertFalse(os.path.exists(folder[dir]))

        folder.setup()
        for dir in folder.FOLDERS:
            self.assertTrue(os.path.exists(folder[dir]))

    def test_small_setup(self):
        tmpdir = self.mkdtemp()
        root = os.path.join(tmpdir, 'test')
        folder = WorkFolder(root=root)
        self.assertFalse(os.path.exists(root))

        folder.setup(False)
        self.assertTrue(os.path.exists(folder.root))
        for dir in folder.FOLDERS:
            self.assertFalse(os.path.exists(folder[dir]))

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
