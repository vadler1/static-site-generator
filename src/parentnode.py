from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str|None, children: list|None, props: dict | None = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        props = ""
        if self.props:
            props = " " + self.props_to_html()

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag!r}, {self.children!r}, {self.props!r})"
