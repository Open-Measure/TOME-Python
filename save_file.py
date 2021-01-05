# import pickle


def save_file(content, file_path, mode="w", encoding="utf-8"):
    """Wrapper function to write string or binary content to a file."""
    saved_file = open(file_path, mode=mode, encoding=encoding)
    saved_file.write(content)
    # pickle.dump(content, file)
    saved_file.close()
