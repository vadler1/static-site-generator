import unittest
from textnode import TextNode, TextType
from util import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_bold_text(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_italic_text(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_code_text(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_bold_and_italic_text(self):
        text = "This is **bold** and _italic_ text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_bold_and_code_text(self):
        text = "This is **bold** and `code` text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_italic_and_code_text(self):
        text = "This is _italic_ and `code` text"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_image(self):
        text = "This is an ![alt text](image.jpg) image"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "image.jpg"),
            TextNode(" image", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_link(self):
        text = "This is a [link](https://example.com)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]

        self.assertEqual(nodes, expected)

    def test_bootdev_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(nodes, expected)
