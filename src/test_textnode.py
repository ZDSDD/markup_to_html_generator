import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


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

    def test_split_nodes_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
