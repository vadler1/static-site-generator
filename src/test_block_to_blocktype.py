import unittest
from blocktype import BlockType
from parser import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-Item"), BlockType.PARAGRAPH)

    def test_unordered_list_multi(self):
        self.assertEqual(
            block_to_block_type("- Item\n- Item"), BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1.Item"), BlockType.PARAGRAPH)

    def test_ordered_list_sequential(self):
        self.assertEqual(
            block_to_block_type("1. Item\n2. Item"), BlockType.ORDERED_LIST
        )
        self.assertEqual(block_to_block_type("1. Item\n3. Item"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Paragraph"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
