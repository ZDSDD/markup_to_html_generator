from htmlnode import LeafNode
import re
from enum import Enum, auto

class TextType(Enum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()
    
class TextNode:
    def __init__(self, text: str, text_type: str, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return (
            self.text == value.text
            and value.text_type == self.text_type
            and self.url == value.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType)-> list[TextNode]:
    # Escape delimiter for regex
    escaped_delimiter = re.escape(delimiter)
    nodes = []
    for node in old_nodes:
        input_text = node.text
        # Construct the regex pattern dynamically
        pattern = re.compile(f'{escaped_delimiter}(.*?){escaped_delimiter}')
        
        last_end = 0
        
        for match in pattern.finditer(input_text):
            # Add the text before the delimiter
            if match.start() > last_end:
                nodes.append(TextNode(input_text[last_end:match.start()], TextType.TEXT))
            
            # Add the text between delimiters
            nodes.append(TextNode(match.group(1), text_type=text_type))
            last_end = match.end()
        
        # Add the remaining text after the last delimiter
        if last_end < len(input_text):
            nodes.append(TextNode(input_text[last_end:], TextType.TEXT))
    
    return nodes