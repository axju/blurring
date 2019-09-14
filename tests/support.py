import tempfile
import shutil


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
