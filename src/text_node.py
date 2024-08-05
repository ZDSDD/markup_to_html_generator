from .htmlnode import LeafNode
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
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue

            current_text_type = text_type if i % 2 == 1 else TextType.TEXT
            split_nodes.append(TextNode(sections[i], current_text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]):
    result = []

    # here will be a loop over all nodes
    for node in old_nodes:
        links = extract_markdown_images(node.text)
        # If the node doesn't contain any link, just append it to the result list as it is.
        if len(links) == 0:
            result.append(node)
            continue
        text = node.text
        for link in links:
            index_of_link = text.index(link[0])
            len_to_delete = len(link[0]) + len(link[1]) + 4  # brackets
            text_node = text[0 : index_of_link - 2]
            text = text[index_of_link - 1 :]
            if text_node != "":
                result.append(TextNode(text=text_node, text_type=TextType.TEXT))
            if link[0] != "":
                result.append(
                    TextNode(text=link[0], url=link[1], text_type=TextType.IMAGE)
                )
            text = text[len_to_delete:]
        
        if len(text) > 0:
            result.append(TextNode(text=text, text_type=TextType.TEXT))
    return result

def split_nodes_link(old_nodes: list[TextNode]):
    result = []

    # here will be a loop over all nodes
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        # If the node doesn't contain any link, just append it to the result list as it is.
        if len(links) == 0:
            result.append(node)
            continue

        text = node.text
        for link in links:
            index_of_link = text.index(link[0])
            len_to_delete = len(link[0]) + len(link[1]) + 4  # brackets
            text_node = text[0 : index_of_link - 1]
            text = text[index_of_link - 1 : -1]
            if text_node != "":
                result.append(TextNode(text=text_node, text_type=TextType.TEXT))
            if link[0] != "":
                result.append(
                    TextNode(text=link[0], url=link[1], text_type=TextType.LINK)
                )

            text = text[len_to_delete:]

    return result
    


def text_to_textnodes(text):
    result = [TextNode(text,TextType.TEXT)]
    result = split_nodes_delimiter(result, '**', TextType.BOLD)
    result = split_nodes_delimiter(result, '*', TextType.ITALIC)
    result = split_nodes_delimiter(result, '`', TextType.CODE)
    result = split_nodes_link(result)
    result = split_nodes_image(result)
    return result


def print_nodes(nodes, title = 'niestety nie ma tytlu :()'):
    print(title)
    for node in nodes:
        print(node)
    print()
    print()