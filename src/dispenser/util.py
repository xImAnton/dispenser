import os


def create_file_if_not_exists(path: str, empty_content: str = "") -> None:
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(str(empty_content))
