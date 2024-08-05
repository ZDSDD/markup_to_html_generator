import unittest

from src.text_node import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("this is text node", "italic")
        self.assertEqual(node.url, None)

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is only text", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), "This is only text")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<b>This is bold text</b>"
        )

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        self.assertEqual(
            text_node_to_html_node(node).to_html(), "<i>This is italic text</i>"
        )

    def test_text_node_to_html_node_code(self):
        node = TextNode("--c++", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>--c++</code>")

    def test_text_node_to_html_node_link(self):
        node = TextNode(
            url="http://google.com", text_type=TextType.LINK, text="nice site"
        )
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<a href="http://google.com">nice site</a>',
        )

    def test_text_node_to_html_node_image(self):
        node = TextNode(
            url="http://google.com/image/plant.jpg",
            text_type=TextType.IMAGE,
            text="nice plant",
        )
        self.assertEqual(
            text_node_to_html_node(node).to_html(),
            '<img src="http://google.com/image/plant.jpg" alt="nice plant"></img>',
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(result, expected)

# if __name__ == "__main__":
#     unittest.main()
