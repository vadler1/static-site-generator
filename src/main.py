import os
import shutil
import sys
from copystatic import copy_folder
from generate_page import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Basepath: {basepath}")

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_folder(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path=dir_path_public, basepath=basepath)

if __name__ == "__main__":
    main()
