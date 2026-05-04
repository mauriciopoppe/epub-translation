import unittest
import os
import shutil
import tempfile
import zipfile
from ..scripts.epub_manager import extract_epub, pack_epub

class TestEpubManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.input_epub = os.path.join(self.test_dir, "test.epub")
        self.extract_dir = os.path.join(self.test_dir, "extracted")
        self.output_epub = os.path.join(self.test_dir, "output.epub")
        
        # Create a dummy EPUB (zip)
        with zipfile.ZipFile(self.input_epub, 'w') as zip_ref:
            zip_ref.writestr('mimetype', 'application/epub+zip')
            zip_ref.writestr('META-INF/container.xml', '<xml></xml>')
            zip_ref.writestr('OEBPS/content.opf', '<xml></xml>')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_extract_epub(self):
        extract_epub(self.input_epub, self.extract_dir)
        self.assertTrue(os.path.exists(os.path.join(self.extract_dir, 'mimetype')))
        self.assertTrue(os.path.exists(os.path.join(self.extract_dir, 'OEBPS/content.opf')))

    def test_pack_epub(self):
        extract_epub(self.input_epub, self.extract_dir)
        pack_epub(self.extract_dir, self.output_epub)
        
        self.assertTrue(os.path.exists(self.output_epub))
        with zipfile.ZipFile(self.output_epub, 'r') as zip_ref:
            # Check mimetype is first and uncompressed
            info = zip_ref.getinfo('mimetype')
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(zip_ref.namelist()[0], 'mimetype')

if __name__ == "__main__":
    unittest.main()
