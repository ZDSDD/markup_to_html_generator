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
    dest_dir = os.path.dirname(dest_path)  # Get the directory part of the path
    os.makedirs(dest_dir, exist_ok=True)   # Create the directory if it doesn't exist        
    with open(dest_path, 'w', encoding="utf-8") as file:
        file.write(content_with_everything)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Convert paths to Path objects
    dir_path_content = Path(dir_path_content)
    dest_dir_path = Path(dest_dir_path)
    
    # Walk through each directory and its subdirectories
    for root, dirs, files in os.walk(dir_path_content):
        root = Path(root)
        # Process each file
        for file in files:
            # Full relative path to the file
            file_path: Path = root / file
            print("filepath", file_path)
            print('[0]', file_path.parts[1:])
            
            # Define the output HTML file path, replacing .md with .html
            output_file_path = dest_dir_path.joinpath(*file_path.parts[1:-1], file.replace('.md', '.html'))
            
            # Generate the page (assuming generate_page is defined elsewhere)
            generate_page(file_path, template_path, output_file_path)

def main(args=None):
    src_path = Path("./static")
    des_path = Path("./public")
    os.makedirs(des_path, exist_ok=True)
    shutil.rmtree(des_path)
    shutil.copytree(src_path, des_path)
    generate_pages_recursive(
        "./content",
        "./template.html",
        "./public",
    )


if __name__ == "__main__":
    main()
