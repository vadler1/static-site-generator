import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello", props={"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello</p>')

    def test_to_html_with_value_only(self):
        node = LeafNode(tag=None, value="Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_without_value_raises(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
