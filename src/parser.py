import re
from blocktype import BlockType, block_type_patterns
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )

    raise NotImplementedError(f"Unsupported text type: {text_node.text_type}")


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


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()

        if stripped_block == "":
            continue

        filtered_blocks.append(stripped_block)

    return filtered_blocks





def block_to_block_type(md: str) -> BlockType:
    if re.match(block_type_patterns[BlockType.HEADING], md):
        return BlockType.HEADING

    if re.match(block_type_patterns[BlockType.CODE], md):
        return BlockType.CODE

    if re.match(block_type_patterns[BlockType.QUOTE], md):
        return BlockType.QUOTE


    if re.match(block_type_patterns[BlockType.UNORDERED_LIST], md):
        return BlockType.UNORDERED_LIST

    ol_matches = re.findall(block_type_patterns[BlockType.ORDERED_LIST], md)
    if ol_matches:
        # ensure counter is incrementing
        i = 0
        for match in ol_matches:
            if int(match[0]) != i + 1:
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                html_nodes.append(markdown_to_heading(block))
            case BlockType.CODE:
                html_nodes.append(markdown_to_code(block))
            case BlockType.QUOTE:
                html_nodes.append(markdown_to_quote(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(markdown_to_unordered_list(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(markdown_to_ordered_list(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(markdown_to_paragraph(block))

    parent_node = ParentNode(tag="div", children=html_nodes)
    return parent_node


def text_to_children(text: str) -> list[HTMLNode]:
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))

    return children


def markdown_to_paragraph(markdown: str) -> HTMLNode:
    # replace \n with whitespace
    markdown = markdown.replace("\n", " ")
    return ParentNode(tag="p", children=text_to_children(markdown))


def markdown_to_heading(markdown: str) -> HTMLNode:
    match = re.match(block_type_patterns[BlockType.HEADING], markdown)
    if not match:
        raise ValueError("Invalid heading markdown")

    level = len(match.group(1))
    value = match.group(2).replace("\n", " ")
    return ParentNode(tag=f"h{level}", children=text_to_children(value))


def markdown_to_code(markdown: str) -> HTMLNode:
    match = re.match(block_type_patterns[BlockType.CODE], markdown)
    if not match:
        raise ValueError("Invalid code block markdown")

    return ParentNode(tag="pre", children=[LeafNode(tag="code", value=match.group(1))])


def markdown_to_quote(markdown: str) -> HTMLNode:
    match = re.match(block_type_patterns[BlockType.QUOTE], markdown)
    if not match:
        raise ValueError("Invalid quote markdown")

    value = match.group(1)
    return ParentNode(tag="blockquote", children=text_to_children(value))


def markdown_to_unordered_list(markdown: str) -> HTMLNode:
    items = re.findall(block_type_patterns[BlockType.UNORDERED_LIST], markdown)
    children = [ParentNode(tag="li", children=text_to_children(item)) for item in items]
    return ParentNode(tag="ul", children=children)


def markdown_to_ordered_list(markdown: str) -> HTMLNode:
    items = re.findall(block_type_patterns[BlockType.ORDERED_LIST], markdown)
    children = [ParentNode(tag="li", children=text_to_children(item)) for _, item in items]
    return ParentNode(tag="ol", children=children)
