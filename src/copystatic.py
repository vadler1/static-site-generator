import shutil
import os

def copy_folder(src: str, dst: str):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)

        print(f"[copy_folder] {src_path} -> {dst_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_folder(src_path, dst_path)
