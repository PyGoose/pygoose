import os
from distutils import dir_util

def copy_static_files(static_src_path,dist_src_path):
    try:
        os.makedirs(dist_src_path, exist_ok=True)
    except:
        pass
    try:
        dir_util.copy_tree(static_src_path,dist_src_path)
    except Exception as Err:
        raise Err
