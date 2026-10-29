from parser import markdown_to_html_node, extract_title
import os


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"[generate_page] {from_path} -> {dest_path} | template: {template_path}")

    with open(from_path, "r") as f:
        content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)


    for file in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, file)
        dst_path = os.path.join(dest_dir_path, file)

        print(f"[generate_pages_recursive] {src_path} -> {dst_path}")
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dst_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(src_path, template_path, dst_path)
