from contextlib import AbstractContextManager
from typing import Any
import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


node = HTMLNode(
"This is a text node",
"bold",
props={
    "href": "https://www.google.com",
    "target": "_blank",
},
)
class TestHTMLNode(unittest.TestCase):

            
    def test_props_to_html(self):
        self.assertEqual(node.props_to_html(),  'href="https://www.google.com" target="_blank"')


    def test_repr(self):
        self.assertEqual(f'{node}', f'HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})')
        

    def test_to_html(self):
        actual1=LeafNode("p", "This is a paragraph of text.")
        actual2=LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        self.assertEqual(actual1.to_html(), '<p>This is a paragraph of text.</p>')
        self.assertEqual(actual2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_tag(self):
        node = ParentNode(
            tag="p",
            children=
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_tag(self):
        node = ParentNode(
            tag="p",
            children=
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props={"color":"red", "class": "cv-21231 ad312 zxc fads"}
        )

        self.assertEqual(node.to_html(), '<p color="red" class="cv-21231 ad312 zxc fads"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_tag_and_children_tag(self):
        node = ParentNode(
            tag="p",
            children=
            [
                LeafNode("b", "Bold text",{"color" : "green"}),
                LeafNode(None, "Normal text", {"class": "nothing personal kid"}),
                LeafNode("i", "italic text", {"id": "footer"}),
                LeafNode(None, "Normal text"),
            ],
            props={"color":"red", "class": "cv-21231 ad312 zxc fads"}
        )

        self.assertEqual(node.to_html(), '<p color="red" class="cv-21231 ad312 zxc fads"><b color="green">Bold text</b>Normal text<i id="footer">italic text</i>Normal text</p>')

    def test_no_children_raise_error(self):
        
        node = ParentNode(
            tag="p",
            children=
            [
            ],
            props={"color":"red", "class": "cv-21231 ad312 zxc fads"}
        )
        
        self.assertRaises(ValueError, node.to_html)


    def test_no_children_raise_error(self):
        
        node = ParentNode(
            tag="",
            children=
            [
                LeafNode("b", "Bold text",{"color" : "green"}),
                LeafNode(None, "Normal text", {"class": "nothing personal kid"}),
                LeafNode("i", "italic text", {"id": "footer"}),
                LeafNode(None, "Normal text"),
            ],
            props={"color":"red", "class": "cv-21231 ad312 zxc fads"}
        )
        
        self.assertRaises(ValueError, node.to_html)

# if __name__ == '__main__':
#     unittest.main()