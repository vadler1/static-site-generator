from platform import node

from textnode import TextNode, TextType
from util import extract_markdown_images, split_nodes_delimiter, extract_markdown_links, split_nodes_image


def main():
    node1 = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
    node2 = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ",TextType.TEXT)
    node3 = TextNode("asd ![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)
    nodes = [node1, node2, node3]
    nodes = split_nodes_image(nodes)
    print(nodes)

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    link_tuples = extract_markdown_links(text)
    print(link_tuples)


if __name__ == "__main__":
    main()
