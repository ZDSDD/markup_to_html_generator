from enum import Enum, auto

from htmlnode import HTMLNode, ParentNode, LeafNode
from text_node import TextNode, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_block(markdown: str) -> list[str]:
    return markdown.split("\n\n")

def extract_title(markdown: str):
    blocks = markdown_to_block(markdown)
    for block in blocks:
        if isHeading(block) and get_heading_level(block) == 1:
            return format_heading_to_html(block)
    raise Exception("No title")

def block_to_block_type(text_block: str) -> BlockType:
    if isHeading(text_block):
        return BlockType.HEADING
    elif isCode(text_block):
        return BlockType.CODE
    elif isQuote(text_block):
        return BlockType.QUOTE
    elif isOrderedList(text_block):
        return BlockType.ORDERED_LIST
    elif isUnOrderedList(text_block):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def isOrderedList(text_block: str):
    lines = text_block.split("\n")
    for index, line in enumerate(lines, start=1):
        if len(line) < 3:
            return False
        if line[0] != str(index):
            return False
        if line[2] != " ":
            return False

    return True


def isUnOrderedList(text_block: str):
    lines = text_block.split("\n")
    for line in lines:
        if len(line) < 1:
            return False
        if line[0] != "*" and line[0] != "-":
            return False
        if line[1] != " ":
            return False
    return True


def isQuote(string: str):
    return string[0] == ">"


def isCode(string: str):
    string = string.strip()
    if len(string) < 6:
        return False
    return string[:3] == "```" and string[-3:] == "```"


def isHeading(string: str) -> bool:

    if len(string) < 2:
        return False
    if string[0] != "#":
        return False

    counter = 0

    for character in string:
        if character == "#":
            counter += 1
        else:
            break
        if counter > 6:
            return False
    return True


def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_block(markdown)
    blocks = [block.strip('\n') for block in blocks]
    child_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            child_nodes.append(ParentNode(f'h{get_heading_level(block)}', get_nodes_from_block(format_heading_to_html(block))))
        if block_type == BlockType.CODE:
            child_nodes.append(ParentNode("pre", [ParentNode("Code", get_nodes_from_block(format_code_for_html(block)))]))
        if block_type == BlockType.QUOTE:
            child_nodes.append(ParentNode("blockquote", get_nodes_from_block(format_quote_to_html(block))))
        if block_type == BlockType.UNORDERED_LIST:
            child_nodes.append(ParentNode('ul', get_nodes_for_list(format_un_ordered_list_to_html(block))))
        if block_type == BlockType.ORDERED_LIST:
            child_nodes.append(ParentNode('ol', get_nodes_for_list(format_ordered_list_to_html(block))))
        if block_type == BlockType.PARAGRAPH:
            child_nodes.append(ParentNode('p', get_nodes_from_block(block)))
                

    return ParentNode('div', child_nodes)

def get_nodes_for_list(list_items):
    return [ParentNode('li', get_nodes_from_block(item)) for item in list_items]

def get_nodes_from_block(block):
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(block)]

def get_heading_level(block: str) -> int:
    counter:int = 0
    for character in block:
        if character == '#':
            counter += 1
        else:
            break
    return counter

def format_heading_to_html(block: str) -> str:
    return block[get_heading_level(block) + 1:]

def format_un_ordered_list_to_html(block: str) -> list[str]:
    return [str[2:] for str in block.split('\n')]

def format_ordered_list_to_html(block: str) -> list[str]:
    return [str[3:] for str in block.split('\n')]

def format_code_for_html(code_block):
    return code_block[3:-3]


def format_quote_to_html(code_block):
    return code_block[1:].strip('\n').strip()
