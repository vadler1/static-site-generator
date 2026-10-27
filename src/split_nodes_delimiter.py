
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # Skip nodes that are not plain text - add them as is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        num_parts = len(parts)
        if num_parts > 1 and num_parts % 2 == 0:
            raise Exception("Unmatched delimiter found")

        for i in range(num_parts):
            part = parts[i]
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
