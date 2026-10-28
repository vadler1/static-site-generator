import unittest
from parser import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):

        markdown = "This is a paragraph.\n\nThis is another paragraph."
        expected = ["This is a paragraph.", "This is another paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_bootdev_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_empty_markdown(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_excessive_newlines(self):
        md = "This is a paragraph.\n\n\n\n\nThis is another paragraph."
        expected = ["This is a paragraph.", "This is another paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)
