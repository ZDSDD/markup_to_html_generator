from enum import Enum, auto


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    quote = auto()
    unordered_list = auto()
    ordered_list = auto()


def markdown_to_block(markdown: str) -> list[str]:
    return markdown.split("\n\n")


def block_to_block_type(text_block: str) -> BlockType:
    if isHeading(text_block):
        return BlockType.HEADING
    elif isCode(text_block):
        return BlockType.CODE

    return BlockType.PARAGRAPH


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
