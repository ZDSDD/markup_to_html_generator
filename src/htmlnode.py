class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children=None, props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        result: str = ""
        if self.props is not None:
            result = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return result

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict[str, str] = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError('Value cannot be None')
        if self.tag is None or self.tag == "":
            return self.value
        
        props = self.props_to_html()
        if props:
            props = " " + props
        return f'<{self.tag}{props}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag: str,children: list[HTMLNode], props: dict[str, str] = None) -> None:
        super().__init__(tag=tag, children=children, props=props)
        
    
    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError('parent node need to have a tag')
        if self.children is None or len(self.children) == 0:
            raise ValueError('parent node needs to have children')
        
        result = self.props_to_html()
        if result != "":
           result = " " + result
        result = f'<{self.tag}{result}>'

        for child in self.children:
            result = result + child.to_html()
        result = f'{result}</{self.tag}>'
        
        return result