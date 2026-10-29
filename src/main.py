import os
import shutil
from copystatic import copy_folder
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_folder(dir_path_static, dir_path_public)

    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")

if __name__ == "__main__":
    main()
