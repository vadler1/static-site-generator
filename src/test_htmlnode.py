import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a different text node")
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = HTMLNode("p", "This is a text node", props={"class": "text","title": "A title"})
        props_str = node.props_to_html()
        self.assertIn('class="text"', props_str)
        self.assertIn('title="A title"', props_str)
        self.assertEqual(props_str, 'class="text" title="A title"')






if __name__ == "__main__":
    unittest.main()
