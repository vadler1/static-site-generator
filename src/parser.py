import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pairs = []

    pattern = r"\!\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    for alt_text, url in matches:
        pairs.append((alt_text, url))

    return pairs


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pairs = []

    pattern = r"\[([^\]]*)\]\(([^\)]*)\)"
    matches = re.findall(pattern, text)
    for link_text, url in matches:
        pairs.append((link_text, url))

    return pairs


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_image_link(old_nodes, TextType.LINK)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_image_link(old_nodes, TextType.IMAGE)


def _split_nodes_image_link(
    old_nodes: list[TextNode], text_type: TextType
) -> list[TextNode]:
    match text_type:
        case TextType.IMAGE:
            extract_func = extract_markdown_images
            split_pattern = lambda alt_text, url: f"![{alt_text}]({url})"
        case TextType.LINK:
            extract_func = extract_markdown_links
            split_pattern = lambda link_text, url: f"[{link_text}]({url})"
        case _:
            raise Exception("Unsupported text type")

    new_nodes = []
    for node in old_nodes:
        # handle non-text nodes by adding them as is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        found_tuples = extract_func(node.text)
        if not found_tuples:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in found_tuples:
            segments = remaining_text.split(split_pattern(alt_text, url), 1)

            if segments[0] != "":
                new_nodes.append(TextNode(segments[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, text_type, url))

            remaining_text = segments[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]

    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes

def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()

        if stripped_block == "":
            continue

        filtered_blocks.append(stripped_block)

    return filtered_blocks
