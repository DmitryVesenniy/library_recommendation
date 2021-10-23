import os


def sort_files(file_name):
    _id = 0
    file_name = os.path.splitext(file_name)[0]
    split_name = file_name.split("_")

    if len(split_name) > 1 and split_name[-1].isdigit():
        _id = int(split_name[-1])

    return _id


def search_files(prefix, suffix, path: str) -> list[str]:
    files = [file_name for file_name in os.listdir(path) if file_name.startswith(prefix) and file_name.endswith(suffix)]

    files.sort(key=sort_files)
    return files
