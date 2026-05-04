import unittest
import os
import shutil
import tempfile
from bs4 import BeautifulSoup
from ..scripts.translate_processor import get_text_nodes, apply_translations, update_metadata

class TestTranslateProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.html_content = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Test</title></head>
<body>
    <p>Hello World</p>
    <p>Section 2</p>
</body>
</html>"""
        self.html_path = os.path.join(self.test_dir, "test.xhtml")
        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(self.html_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_text_nodes(self):
        nodes, soup = get_text_nodes(self.html_path)
        texts = [n.string.strip() for n in nodes]
        self.assertIn("Hello World", texts)
        self.assertIn("Section 2", texts)
        self.assertIn("Test", texts)

    def test_apply_translations(self):
        trans_file = os.path.join(self.test_dir, "trans.txt")
        # Find IDs
        nodes, _ = get_text_nodes(self.html_path)
        # Assuming Test is 0, Hello World is 1, Section 2 is 2
        # But order depends on soup.find_all(string=True)
        id_map = {n.string.strip(): i for i, n in enumerate(nodes)}
        
        with open(trans_file, "w", encoding="utf-8") as f:
            f.write(f"ID:{id_map['Hello World']}|Bonjour le Monde\n")
            f.write(f"ID:{id_map['Section 2']}|Section Deux\n")

        output_path = os.path.join(self.test_dir, "output.xhtml")
        apply_translations(self.html_path, trans_file, output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Bonjour le Monde", content)
            self.assertIn("Section Deux", content)
            self.assertNotIn("Hello World", content)

    def test_update_metadata(self):
        opf_content = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:language>en</dc:language>
  </metadata>
</package>"""
        opf_path = os.path.join(self.test_dir, "content.opf")
        with open(opf_path, "w", encoding="utf-8") as f:
            f.write(opf_content)
        
        update_metadata(opf_path, "fr")
        
        with open(opf_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<dc:language>fr</dc:language>", content)

if __name__ == "__main__":
    unittest.main()
