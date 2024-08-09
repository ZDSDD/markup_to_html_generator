from pathlib import Path
import shutil
import os
from blocks import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Open the file in read mode and read its content
    with open(from_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Now, `content` contains the entire content of the .md file as a string

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    content_with_title = template.replace('{{ Title }}', extract_title(content))
    content_with_everything = content_with_title.replace('{{ Content }}', markdown_to_html_node(content).to_html())
    with open(dest_path, 'w', encoding="utf-8") as file:
        file.write(content_with_everything)


def main(args=None):
    src_path = Path("/home/sebasadowy/bootdev/static_site_gen/static")
    des_path = Path("/home/sebasadowy/bootdev/static_site_gen/public")
    os.makedirs(des_path, exist_ok=True)
    shutil.rmtree(des_path)
    shutil.copytree(src_path, des_path)
    generate_page(
        "/home/sebasadowy/bootdev/static_site_gen/content/index.md",
        "/home/sebasadowy/bootdev/static_site_gen/template.html",
        "/home/sebasadowy/bootdev/static_site_gen/public/index.html",
    )


if __name__ == "__main__":
    main()
