import tempfile
import shutil
import zipfile
import os
import unittest

from Freya_alerce.core.base import Base
import Freya_alerce.files.list_file as files_

class TestCreateModuleApi(unittest.TestCase):
    
    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        path_template_api = Base(source='api').path_files_template_from()
        extract_zip = zipfile.ZipFile(path_template_api)
        listOfFileNames = ['configure.py','methods.py','__init__.py']
        for fileName in listOfFileNames:
            extract_zip.extract(fileName, self.tmp_test.name)
        extract_zip.close()

        list_path = [os.path.join(self.tmp_test.name,'configure.py'),os.path.join(self.tmp_test.name,'methods.py')]
        files_.Files(list_path,'NAME','test').replace_in_files()

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 