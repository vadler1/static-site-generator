import unittest
from textnode import TextNode, TextType
from parser import split_nodes_image, split_nodes_link


class TestSplitNodesLinksImage(unittest.TestCase):
    def test_single_image(self):
        text = "This is an image ![alt](url) in text."
        nodes = split_nodes_image([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" in text.", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_text_before_image(self):
        text = "Text before ![alt](url)"
        nodes = split_nodes_image([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
        ]

        self.assertEqual(nodes, expected)

    def test_text_after_image(self):
        text = "![alt](url) text after"
        nodes = split_nodes_image([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_just_image(self):
        text = "![alt](url)"
        nodes = split_nodes_image([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
        ]

        self.assertEqual(nodes, expected)

    def test_multi_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_link(self):
        text = "This is a link [alt](url) in text."
        nodes = split_nodes_link([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("alt", TextType.LINK, "url"),
            TextNode(" in text.", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_text_before_link(self):
        text = "Text before [alt](url)"
        nodes = split_nodes_link([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt", TextType.LINK, "url"),
        ]

        self.assertEqual(nodes, expected)

    def test_text_after_link(self):
        text = "[alt](url) text after"
        nodes = split_nodes_link([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("alt", TextType.LINK, "url"),
            TextNode(" text after", TextType.TEXT),
        ]

        self.assertEqual(nodes, expected)

    def test_just_link(self):
        text = "[alt](url)"
        nodes = split_nodes_link([TextNode(text, TextType.TEXT)])

        expected = [
            TextNode("alt", TextType.LINK, "url"),
        ]

        self.assertEqual(nodes, expected)

    def test_multi_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
