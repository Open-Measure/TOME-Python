# import pickle
from log_info import log_warning, log_info


def save_file(content, file_path, mode="w", encoding="utf-8"):
    """Wrapper function to write string or binary content to a file."""
    if content is None:
        log_warning(f"File content is empty: save_file({content}, {file_path}, {mode}, {encoding})")
    else:
        saved_file = open(file_path, mode=mode, encoding=encoding)
        saved_file.write(content)
        # pickle.dump(content, file)
        saved_file.close()
