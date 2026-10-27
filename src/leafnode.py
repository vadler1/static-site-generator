
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str|None, props: dict|None=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value


        props = ""
        if self.props:
            props = " " + self.props_to_html()

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag!r}, {self.value!r}, {self.props!r})"
