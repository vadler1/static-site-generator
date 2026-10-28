import unittest
from parser import extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multi_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_multi_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_tuples = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(link_tuples, expected)
