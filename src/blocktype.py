import enum
import re

class BlockType(enum.Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

block_type_patterns: dict[BlockType, re.Pattern[str]] = {
    BlockType.HEADING: re.compile(r"^(#{1,6}) (.*)"),
    BlockType.CODE: re.compile(r"^\`{3}\n((?:[^`]|\n)*)`{3}$"),
    BlockType.QUOTE: re.compile(r"^> ?(.*)"),
    BlockType.UNORDERED_LIST: re.compile(r"^- (.*)", re.MULTILINE),
    BlockType.ORDERED_LIST: re.compile(r"^(\d)+\. (.*)$", re.MULTILINE),
}
