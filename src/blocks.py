from enum import Enum, auto
import re

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_block(markdown: str) -> list[str]:
    return markdown.split("\n\n")


def block_to_block_type(text_block: str) -> BlockType:
    if isHeading(text_block):
        return BlockType.HEADING
    elif isCode(text_block):
        return BlockType.CODE
    elif isQuote(text_block):
        return BlockType.QUOTE
    elif isOrderedList(text_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def isOrderedList(text_block: str):
    lines = text_block.split('\n')
    for index, line in enumerate(lines, start=1):
        if len(line) < 3:
            return False
        if line[0] != str(index):
            return False
        if line[2] != ' ':
            return False
    return True

def isQuote(string :str):
    return string[0] == '>'

def isCode(string: str):
    string = string.strip()
    if len(string) < 6:
        return False
    return string[:3] == "```" and string[-3:] == "```"


def isHeading(string: str) -> bool:
    if len(string) < 2:
        return False
    if string[0] != " " or string[1] != "#":
        return False

    counter = 0

    for character in string[1:]:
        if character == "#":
            counter += 1
        else:
            break
        if counter > 6:
            return False
    return True
