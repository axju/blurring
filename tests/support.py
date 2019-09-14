import os
import tempfile
import shutil


DATADIR = os.path.join(os.path.dirname(__file__), 'data')


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
