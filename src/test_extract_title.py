import unittest
from src.parser import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nSome content"
        self.assertEqual(extract_title(markdown), "Title")

    def test_no_title(self):
        markdown = "## Subtitle\n\nSome content"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_bootdev_example(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

if __name__ == "__main__":
    unittest.main()
