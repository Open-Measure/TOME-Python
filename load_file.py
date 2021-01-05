# import pickle
from log_info import log_info


def load_file(file_path, mode="r", encoding="utf-8"):
    """Wrapper function to a load the content of a file"""
    log_info(f"load_file({file_path},{mode},{encoding})")
    with open(file_path, mode=mode, encoding=encoding) as loaded_file:
        file_content = loaded_file.read()
        # dict = pickle.load(file)
        return file_content
