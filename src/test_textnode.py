import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("this is text node", 'italic')
        self.assertEqual(node.url, None)

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is only text", "text")
        self.assertEqual(text_node_to_html_node(node).to_html(),'This is only text')

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold text", "bold")
        self.assertEqual(text_node_to_html_node(node).to_html(),'<b>This is bold text</b>')

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic text", "italic")
        self.assertEqual(text_node_to_html_node(node).to_html(),'<i>This is italic text</i>')
    
    def test_text_node_to_html_node_code(self):
        node = TextNode("--c++", "code")
        self.assertEqual(text_node_to_html_node(node).to_html(),'<code>--c++</code>')

    def test_text_node_to_html_node_link(self):
        node = TextNode(url="http://google.com", text_type="link", text='nice site')
        self.assertEqual(text_node_to_html_node(node).to_html(),'<a href="http://google.com">nice site</a>')

    def test_text_node_to_html_node_image(self):
        node = TextNode(url="http://google.com/image/plant.jpg", text_type="image", text='nice plant')
        self.assertEqual(text_node_to_html_node(node).to_html(),'<img src="http://google.com/image/plant.jpg" alt="nice plant"></img>')
    
if __name__ == "__main__":
    unittest.main()