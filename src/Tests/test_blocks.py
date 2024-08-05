import unittest

from src.blocks import block_to_block_type, markdown_to_block, BlockType

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        str = """\
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item\
"""
        result = markdown_to_block(str)
        expected = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    """\
* This is the first list item in a list block
* This is a list item
* This is another list item\
"""]
        self.assertListEqual(expected,result)

    # HEADINGS
    def test_no_heading(self):
        self.assertEqual(block_to_block_type("cos tam"), BlockType.PARAGRAPH)
    def test_too_many_heading(self):
        self.assertEqual(block_to_block_type(" #######cos tam"), BlockType.PARAGRAPH)
    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#cos tam"), BlockType.PARAGRAPH)
    def test_heading_solo(self):
        self.assertEqual(block_to_block_type(" #cos tam"), BlockType.HEADING)
    def test_heading_duo(self):
        self.assertEqual(block_to_block_type(" ##cos tam"), BlockType.HEADING)
    def test_heading_trio(self):
        self.assertEqual(block_to_block_type(" ###cos tam"), BlockType.HEADING)
    def test_heading_quartet(self):
        self.assertEqual(block_to_block_type(" ####cos tam"), BlockType.HEADING)
    def test_heading_quintet(self):
        self.assertEqual(block_to_block_type(" #####cos tam"), BlockType.HEADING)
    def test_heading_sextet(self):
        self.assertEqual(block_to_block_type(" ######cos tam"), BlockType.HEADING)


    # CODE BLOCKS
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```this is code```"), BlockType.CODE)
    def test_code_block(self):
        self.assertEqual(block_to_block_type("""
                                            ```
                                            this is code
                                            ```
                                             """), BlockType.CODE)